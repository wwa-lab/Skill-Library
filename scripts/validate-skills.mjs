#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const rootDir = process.cwd();
const skillsDir = path.join(rootDir, "skills");
const namePattern = /^[a-z0-9][a-z0-9-]*$/;

const args = new Set(process.argv.slice(2));
const strict = args.has("--strict");

function normalizeSkillDirName(dirName) {
  return dirName.replace(/^_+/, "");
}

function expectedSkillName(domain, skillDirName) {
  return `${domain}-${normalizeSkillDirName(skillDirName)}`;
}

function expectedSkillNameForStrategy(domain, skillDirName, nameStrategy) {
  if (nameStrategy === "preserve") {
    return normalizeSkillDirName(skillDirName);
  }

  return expectedSkillName(domain, skillDirName);
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

  return {
    data,
    body: content.slice(end + "\n---".length).trim(),
  };
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
  const entries = await fs.readdir(targetPath, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

async function readDomainConfig(domainPath) {
  const configPath = path.join(domainPath, "domain.json");

  if (!(await pathExists(configPath))) {
    return { nameStrategy: "prefix" };
  }

  const config = JSON.parse(await fs.readFile(configPath, "utf8"));
  const nameStrategy = config.nameStrategy ?? "prefix";

  if (!["prefix", "preserve"].includes(nameStrategy)) {
    throw new Error(
      `${path.relative(rootDir, configPath)}: nameStrategy must be "prefix" or "preserve"`,
    );
  }

  return { ...config, nameStrategy };
}

async function discoverSkills() {
  if (!(await pathExists(skillsDir))) {
    return [];
  }

  const skills = [];
  const domains = await listDirectories(skillsDir);

  for (const domain of domains) {
    const domainPath = path.join(skillsDir, domain);
    const domainConfig = await readDomainConfig(domainPath);
    const skillDirs = await listDirectories(domainPath);

    for (const skillDir of skillDirs) {
      const skillPath = path.join(domainPath, skillDir);
      const skillFile = path.join(skillPath, "SKILL.md");

      if (await pathExists(skillFile)) {
        skills.push({ domain, domainConfig, skillDir, skillPath, skillFile });
      }
    }
  }

  return skills;
}

function relative(targetPath) {
  return path.relative(rootDir, targetPath);
}

function addMessage(messages, skill, message) {
  messages.push(`${relative(skill.skillFile)}: ${message}`);
}

async function validateSkill(skill, errors, warnings) {
  if (!namePattern.test(skill.domain)) {
    addMessage(errors, skill, `domain "${skill.domain}" must be lowercase kebab-case`);
  }

  const normalizedDirName = normalizeSkillDirName(skill.skillDir);
  if (!normalizedDirName || !namePattern.test(normalizedDirName)) {
    addMessage(errors, skill, `skill directory "${skill.skillDir}" must normalize to lowercase kebab-case`);
  }

  const content = await fs.readFile(skill.skillFile, "utf8");
  const parsed = parseFrontmatter(content);

  if (!parsed) {
    addMessage(errors, skill, "missing YAML frontmatter delimited by ---");
    return;
  }

  const { name, description, metadata } = parsed.data;
  const expectedName = expectedSkillNameForStrategy(
    skill.domain,
    skill.skillDir,
    skill.domainConfig.nameStrategy,
  );

  if (!name) {
    addMessage(errors, skill, "frontmatter is missing required field: name");
  } else if (name !== expectedName) {
    addMessage(errors, skill, `frontmatter name must be "${expectedName}", found "${name}"`);
  }

  if (!description) {
    addMessage(errors, skill, "frontmatter is missing required field: description");
  } else {
    if (description.length < 40) {
      addMessage(warnings, skill, "description is short; include clear trigger conditions");
    }

    if (!/\b(Use when|Use this|Use for|Use to|Use whenever|Also trigger|Trigger on)\b/i.test(description)) {
      addMessage(warnings, skill, "description should include trigger wording such as \"Use when\" or \"Use this skill whenever\"");
    }
  }

  if (!metadata || typeof metadata !== "object" || Array.isArray(metadata)) {
    addMessage(warnings, skill, "frontmatter should include metadata with author, maintainer, and domain");
  } else {
    for (const key of ["author", "maintainer", "domain"]) {
      if (!metadata[key]) {
        addMessage(warnings, skill, `metadata is missing recommended field: ${key}`);
      }
    }

    if (metadata.domain && metadata.domain !== skill.domain) {
      addMessage(warnings, skill, `metadata.domain should be "${skill.domain}", found "${metadata.domain}"`);
    }
  }

  if (!parsed.body) {
    addMessage(errors, skill, "SKILL.md body is empty");
  } else if (!/^#\s+/m.test(parsed.body)) {
    addMessage(warnings, skill, "SKILL.md body should include a top-level heading");
  }
}

async function main() {
  const skills = await discoverSkills();
  const errors = [];
  const warnings = [];

  if (skills.length === 0) {
    console.warn("No skills found under skills/<domain>/<skill>/SKILL.md");
    return;
  }

  for (const skill of skills) {
    await validateSkill(skill, errors, warnings);
  }

  if (warnings.length > 0) {
    console.warn("\nWarnings:");
    for (const warning of warnings) {
      console.warn(`  - ${warning}`);
    }
  }

  if (errors.length > 0) {
    console.error("\nErrors:");
    for (const error of errors) {
      console.error(`  - ${error}`);
    }
    process.exit(1);
  }

  if (strict && warnings.length > 0) {
    console.error("\nStrict mode failed because warnings were found.");
    process.exit(1);
  }

  console.log(`Validated ${skills.length} skill${skills.length === 1 ? "" : "s"}.`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
