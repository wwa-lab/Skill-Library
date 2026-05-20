#!/usr/bin/env node

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(scriptDir, "..");
const skillsDir = path.join(rootDir, "skills");
const markerFileName = ".skill-library-source.json";
const managedBy = "Skill-Library";
const defaultDest = path.join(os.homedir(), ".config", "opencode", "skills");
const opencodeSkillNamePattern = /^[a-z0-9]+(-[a-z0-9]+)*$/;

function printHelp() {
  console.log(`Usage: node scripts/install-opencode-skills.mjs [options]

Options:
  --domain <name>       Install one family/domain. Can be repeated. Aliases such as ibm-i are supported.
  --project <path>      Install into another repo's .opencode/skills directory.
  --dest <path>         Install destination. Defaults to ~/.config/opencode/skills.
  --include-examples    Include skill directories that start with "_".
  --dry-run             Print planned actions without writing files.
  --force               Overwrite existing destination folders without this repository's marker.
  --help                Show this help.
`);
}

function expandHome(targetPath) {
  if (targetPath === "~") {
    return os.homedir();
  }

  if (targetPath.startsWith("~/")) {
    return path.join(os.homedir(), targetPath.slice(2));
  }

  return path.resolve(targetPath);
}

function parseArgs(argv) {
  const options = {
    domains: [],
    dest: defaultDest,
    destProvided: false,
    project: null,
    includeExamples: false,
    dryRun: false,
    force: false,
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];

    if (arg === "--domain") {
      const value = argv[index + 1];
      if (!value) {
        throw new Error("--domain requires a value");
      }
      options.domains.push(value);
      index += 1;
    } else if (arg === "--project") {
      const value = argv[index + 1];
      if (!value) {
        throw new Error("--project requires a value");
      }
      options.project = expandHome(value);
      index += 1;
    } else if (arg === "--dest") {
      const value = argv[index + 1];
      if (!value) {
        throw new Error("--dest requires a value");
      }
      options.dest = expandHome(value);
      options.destProvided = true;
      index += 1;
    } else if (arg === "--include-examples") {
      options.includeExamples = true;
    } else if (arg === "--dry-run") {
      options.dryRun = true;
    } else if (arg === "--force") {
      options.force = true;
    } else if (arg === "--help" || arg === "-h") {
      options.help = true;
    } else {
      throw new Error(`Unknown option: ${arg}`);
    }
  }

  if (options.project && options.destProvided) {
    throw new Error("Use either --project or --dest, not both");
  }

  if (options.project) {
    options.dest = path.join(options.project, ".opencode", "skills");
  }

  return options;
}

function parseFrontmatter(content) {
  if (!content.startsWith("---\n")) {
    return null;
  }

  const end = content.indexOf("\n---", 4);
  if (end === -1) {
    return null;
  }

  const block = content.slice(4, end).trimEnd();
  const data = {};
  const lines = block.split(/\r?\n/);

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) {
      continue;
    }

    const [, key, rawValue] = match;
    const value = rawValue.trim();

    if (value === ">" || value === "|") {
      const blockLines = [];

      while (index + 1 < lines.length && /^\s+/.test(lines[index + 1])) {
        index += 1;
        blockLines.push(lines[index].trim());
      }

      data[key] = value === ">" ? blockLines.join(" ").trim() : blockLines.join("\n").trim();
    } else if (value === "") {
      const map = {};

      while (index + 1 < lines.length && /^\s+/.test(lines[index + 1])) {
        index += 1;
        const nestedLine = lines[index].trim();
        const nestedMatch = nestedLine.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);

        if (nestedMatch) {
          const [, nestedKey, nestedRawValue] = nestedMatch;
          map[nestedKey] = nestedRawValue.replace(/^['"]|['"]$/g, "").trim();
        }
      }

      data[key] = map;
    } else {
      data[key] = value.replace(/^['"]|['"]$/g, "").trim();
    }
  }

  return data;
}

async function pathExists(targetPath) {
  try {
    await fs.access(targetPath);
    return true;
  } catch {
    return false;
  }
}

async function listDirectories(targetPath) {
  if (!(await pathExists(targetPath))) {
    return [];
  }

  const entries = await fs.readdir(targetPath, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

async function readDomainConfig(domainPath) {
  const configPath = path.join(domainPath, "domain.json");

  if (!(await pathExists(configPath))) {
    return { aliases: [] };
  }

  const config = JSON.parse(await fs.readFile(configPath, "utf8"));
  const aliases = Array.isArray(config.aliases) ? config.aliases : [];
  return { ...config, aliases };
}

async function discoverSkills(options) {
  const selectedDomains = new Set(options.domains);
  const domains = await listDirectories(skillsDir);
  const skills = [];
  const skipped = [];

  for (const domain of domains) {
    const domainPath = path.join(skillsDir, domain);
    const domainConfig = await readDomainConfig(domainPath);
    const selectableNames = new Set([domain, ...domainConfig.aliases]);

    if (
      selectedDomains.size > 0 &&
      ![...selectedDomains].some((selectedDomain) => selectableNames.has(selectedDomain))
    ) {
      continue;
    }

    const skillDirs = await listDirectories(domainPath);

    for (const skillDir of skillDirs) {
      if (skillDir.startsWith("_") && !options.includeExamples) {
        continue;
      }

      const sourcePath = path.join(domainPath, skillDir);
      const skillFile = path.join(sourcePath, "SKILL.md");

      if (!(await pathExists(skillFile))) {
        skipped.push({
          domain,
          skillDir,
          sourcePath,
          reason: "missing SKILL.md",
        });
        continue;
      }

      const frontmatter = parseFrontmatter(await fs.readFile(skillFile, "utf8"));
      if (!frontmatter?.name) {
        throw new Error(`${path.relative(rootDir, skillFile)} is missing frontmatter name`);
      }

      if (frontmatter.name.length > 64 || !opencodeSkillNamePattern.test(frontmatter.name)) {
        throw new Error(
          `${path.relative(rootDir, skillFile)} has invalid OpenCode skill name "${frontmatter.name}"`,
        );
      }

      skills.push({
        domain,
        skillDir,
        sourcePath,
        skillFile,
        installedName: frontmatter.name,
      });
    }
  }

  return { skills, skipped };
}

async function readMarker(targetPath) {
  const markerPath = path.join(targetPath, markerFileName);

  try {
    return JSON.parse(await fs.readFile(markerPath, "utf8"));
  } catch {
    return null;
  }
}

async function canOverwrite(targetPath, options) {
  if (!(await pathExists(targetPath))) {
    return true;
  }

  if (options.force) {
    return true;
  }

  const marker = await readMarker(targetPath);
  return marker?.managedBy === managedBy;
}

async function installSkill(skill, options) {
  const destinationPath = path.join(options.dest, skill.installedName);
  const relativeSource = path.relative(rootDir, skill.sourcePath);

  if (options.dryRun) {
    console.log(`[dry-run] ${relativeSource} -> ${destinationPath}`);
    return;
  }

  if (!(await canOverwrite(destinationPath, options))) {
    throw new Error(
      `Refusing to overwrite ${destinationPath} because it does not have ${markerFileName}. Use --force if this is intentional.`,
    );
  }

  await fs.mkdir(options.dest, { recursive: true });
  await fs.rm(destinationPath, { recursive: true, force: true });
  await fs.cp(skill.sourcePath, destinationPath, {
    recursive: true,
    filter: (source) => path.basename(source) !== markerFileName,
  });

  const marker = {
    managedBy,
    installedName: skill.installedName,
    sourcePath: relativeSource,
    installedAt: new Date().toISOString(),
  };

  await fs.writeFile(
    path.join(destinationPath, markerFileName),
    `${JSON.stringify(marker, null, 2)}\n`,
    "utf8",
  );

  console.log(`Installed ${skill.installedName}`);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));

  if (options.help) {
    printHelp();
    return;
  }

  const { skills, skipped } = await discoverSkills(options);

  if (skills.length === 0) {
    console.log("No installable skills selected.");
    for (const item of skipped) {
      console.log(`[skip] ${path.relative(rootDir, item.sourcePath)} (${item.reason}; placeholder not installable)`);
    }
    return;
  }

  for (const skill of skills) {
    await installSkill(skill, options);
  }

  for (const item of skipped) {
    console.log(`[skip] ${path.relative(rootDir, item.sourcePath)} (${item.reason}; placeholder not installable)`);
  }

  const skippedSuffix =
    skipped.length > 0
      ? `; skipped ${skipped.length} placeholder${skipped.length === 1 ? "" : "s"}`
      : "";

  console.log(
    `${options.dryRun ? "Planned" : "Installed"} ${skills.length} skill${
      skills.length === 1 ? "" : "s"
    }${skippedSuffix}.`,
  );

  if (!options.dryRun) {
    console.log("Restart OpenCode or start a new session so skill discovery refreshes.");
  }
}

main().catch((error) => {
  console.error(error.message ?? error);
  process.exit(1);
});
