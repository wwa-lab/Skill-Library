# DB2 for i Pattern Recognition Guide

This guide helps identify and extract IBM i DB2 constructs (SQL tables, views, indexes, columns, constraints) when analyzing data models. DB2 for i is the SQL interface to IBM i data; DDS physical/logical files map to SQL tables/views.

## SQL Table Structure

### Basic Format

```sql
CREATE TABLE SCHEMA.TABLENAME (
    COLUMN1 CHARACTER(10) NOT NULL,
    COLUMN2 DECIMAL(9,2) NOT NULL,
    COLUMN3 INTEGER,
    COLUMN4 CHAR(8) DEFAULT CURRENT_DATE,
    COLUMN5 CLOB(32768),
    PRIMARY KEY (COLUMN1, COLUMN2)
);

CREATE INDEX IDX_TABLE_COL3 ON SCHEMA.TABLENAME (COLUMN3 ASC);
```

### Column Data Types

| SQL Type | Equivalent DDS | Meaning | Storage |
| --- | --- | --- | --- |
| CHARACTER(n) or CHAR(n) | nA | Fixed-length text | n bytes |
| VARCHAR(n) | (no direct equivalent) | Variable-length text | up to n bytes |
| NUMERIC(p,s) or DECIMAL(p,s) | pS s | Packed decimal; p=precision, s=scale | (p+1)/2 bytes |
| SMALLINT | 5S 0 | 16-bit signed integer | 2 bytes |
| INTEGER | 9S 0 | 32-bit signed integer | 4 bytes |
| BIGINT | 18S 0 | 64-bit signed integer | 8 bytes |
| REAL | 7F | Single-precision float | 4 bytes |
| DOUBLE | 15F | Double-precision float | 8 bytes |
| DATE | 10A | ISO 8601 date (YYYY-MM-DD) | 10 bytes |
| TIME | 8A | ISO 8601 time (HH:MM:SS) | 8 bytes |
| TIMESTAMP | 26A | ISO 8601 timestamp | 26 bytes |
| CLOB(n) | (no direct equivalent) | Character large object; up to n bytes | variable |
| BLOB(n) | (no direct equivalent) | Binary large object; up to n bytes | variable |

### Constraints

```sql
-- Primary Key: unique identifier
PRIMARY KEY (COLUMN1, COLUMN2)

-- Unique Constraint: alternate key
UNIQUE (COLUMN3)

-- Foreign Key: relationship to parent table
FOREIGN KEY (CUSTNO) REFERENCES CUSTOMER(CUSTNO)

-- Not Null: required column
COLUMN1 CHARACTER(10) NOT NULL

-- Default: default value
COLUMN4 CHAR(8) DEFAULT CURRENT_DATE

-- Check: domain constraint (rarely used on IBM i)
CHECK (AMOUNT > 0)
```

## Logical File Equivalents in SQL

### Simple Logical File -> SQL View

DDS Logical File:
```dds
     A          R LFREC         PFILE(CUSTREC)
     A            CUSTNO
     A            CUSTNAME
     A            ACTIVE_FLAG
     A          K CUSTNO
     A          S ACTIVE_FLAG *EQ 'Y'
```

Equivalent SQL:
```sql
CREATE VIEW ACTIVE_CUSTOMERS AS
    SELECT CUSTNO, CUSTNAME, ACTIVE_FLAG
    FROM CUSTOMER
    WHERE ACTIVE_FLAG = 'Y'
    WITH READ ONLY;

CREATE INDEX IDX_CUST_ACTIVE ON CUSTOMER (CUSTNO) WHERE ACTIVE_FLAG = 'Y';
```

### Join Logical File -> SQL Join View

DDS Join LF:
```dds
     A          R ORDREC        JFILE(CUSTOMER ORDER)
     A            CUSTNO                 FROM CUSTOMER
     A            CUSTNAME               FROM CUSTOMER
     A            ORDNO                  FROM ORDER
     A            ORDDATE                FROM ORDER
     A          J                        Start join
     A            4                      Left outer join
     A          JFLD(CUSTOMER.CUSTNO ORDER.CUSTNO)
     A          K ORDNO
```

Equivalent SQL:
```sql
CREATE VIEW ORDERS_WITH_CUSTOMER AS
    SELECT
        C.CUSTNO, C.CUSTNAME,
        O.ORDNO, O.ORDDATE
    FROM CUSTOMER C
    LEFT OUTER JOIN ORDER O ON C.CUSTNO = O.CUSTNO
    WITH READ ONLY;

CREATE INDEX IDX_ORDCUST_ORD ON ORDER (ORDNO ASC);
```

## SQL Index Structure

### Single-Column Index

```sql
CREATE INDEX IDX_CUSTOMER_CUSTNO ON CUSTOMER (CUSTNO ASC);

CREATE UNIQUE INDEX IDX_CUST_EMAIL ON CUSTOMER (EMAIL);
```

**Interpretation**:
- Index on CUSTNO in ascending order
- Index on EMAIL with unique constraint (alternate key)

### Composite Index

```sql
CREATE INDEX IDX_ORDER_CUST_DATE ON ORDER (CUSTNO ASC, ORDDATE DESC);

CREATE INDEX IDX_ACTIVE_BY_REGION ON CUSTOMER (REGION ASC, ACTIVE_FLAG ASC)
    WHERE ACTIVE_FLAG = 'Y';
```

**Interpretation**:
- Compound index on (CUSTNO ascending, ORDDATE descending)
- Filtered index on active customers by region

## DB2 Metadata Extraction

IBM i catalog view names and columns vary by release and shop tooling. Prefer
source evidence supplied by the IBM i team: DDS, SQL DDL generated from the
object, `DSPFFD`, `DSPFD`, or approved extracts from `QSYS2` catalog views.
Treat the query shapes below as examples to align requested columns, not as
portable commands to run blindly.

### Query to Inspect Tables and Columns

```sql
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    LENGTH,
    NUMERIC_SCALE,
    IS_NULLABLE,
    COLUMN_TEXT
FROM QSYS2.SYSCOLUMNS
WHERE TABLE_SCHEMA = 'MYLIB'
    AND TABLE_NAME = 'MYTABLE'
ORDER BY ORDINAL_POSITION;
```

**Output Columns**:
- TABLE_SCHEMA: Schema (library) name
- TABLE_NAME: Table name
- COLUMN_NAME: Column name
- DATA_TYPE: SQL type
- LENGTH: Column length in bytes
- NUMERIC_SCALE: Decimal places (for DECIMAL types)
- IS_NULLABLE: whether NULL is allowed
- COLUMN_TEXT: Comment on column (if present)

### Query to Inspect Primary Keys

```sql
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    CONSTRAINT_NAME,
    COLUMN_NAME,
    ORDINAL_POSITION
FROM QSYS2.SYSKEYS
WHERE TABLE_SCHEMA = 'MYLIB'
    AND TABLE_NAME = 'MYTABLE'
ORDER BY CONSTRAINT_NAME, ORDINAL_POSITION;
```

### Query to Inspect Foreign Keys

```sql
SELECT
    CONSTRAINT_SCHEMA,
    CONSTRAINT_NAME,
    TABLE_SCHEMA,
    TABLE_NAME,
    UNIQUE_CONSTRAINT_SCHEMA,
    UNIQUE_CONSTRAINT_NAME
FROM QSYS2.SYSREFCST
WHERE TABLE_SCHEMA = 'MYLIB'
    AND TABLE_NAME = 'MYTABLE';
```

### Query to Inspect Indexes

```sql
SELECT
    INDEX_SCHEMA,
    INDEX_NAME,
    TABLE_SCHEMA,
    TABLE_NAME,
    COLUMN_NAME,
    ORDINAL_POSITION,
    ORDERING,
    IS_UNIQUE
FROM QSYS2.SYSINDEXES
WHERE TABLE_SCHEMA = 'MYLIB'
    AND TABLE_NAME = 'MYTABLE'
ORDER BY INDEX_NAME, ORDINAL_POSITION;
```

If the local IBM i release uses different catalog views or column names, ask
the DBA/SME for an approved extract instead of adapting the query by guesswork.

## DSPFFD Output

IBM i's `DSPFFD` (Display File Field Description) command produces a report showing all fields in a physical file or logical file. Example:

```
RECORD NAME . . . . . . . . . . . . CUSTREC

FIELD           TYPE  LENGTH  DECIMAL POSITIONS
CUSTNO          CHAR    10           1   10
CUSTNAME        CHAR    30          11   40
ACTIVE_FLAG     CHAR     1          41   41
```

**Interpretation**:
- CUSTNO: character, length 10, positions 1-10
- CUSTNAME: character, length 30, positions 11-40
- ACTIVE_FLAG: character, length 1, position 41

## Mapping DDS to DB2 SQL

### DDS PF -> SQL Table

| DDS Construct | SQL Equivalent |
| --- | --- |
| Physical File (PF) | CREATE TABLE |
| Record Format | Table definition (name from R card) |
| Field | Column definition |
| Field Type 10A | CHARACTER(10) |
| Field Type 9P2 | DECIMAL(9,2) |
| K lines | Keyed access path; PRIMARY KEY only when UNIQUE/constraint evidence supports it |
| U card (unique) | UNIQUE(...) |
| ALWNULL | NULL (in column definition) |

### DDS LF -> SQL View or Index

| DDS Construct | SQL Equivalent |
| --- | --- |
| Logical File (LF) with SELECT | CREATE VIEW ... WHERE ... |
| LF with alternate key order | CREATE INDEX ..., possibly with column reordering |
| Join LF (JFILE) | CREATE VIEW ... JOIN ... |
| LF JFLD | JOIN ... ON [join condition] |
| UNIQUE in LF | CREATE UNIQUE INDEX ... |

## Evidence Collection for DB2

1. **Source Location**: Identify source of SQL DDL or catalog query
   - DDL file: full path, e.g., `/home/archive/ddl/customer.sql`
   - Catalog query: note the query run and timestamp
   - DSPFFD output: note when DSPFFD was run

2. **Column Metadata**: For each column, capture:
   - Column name (exact spelling)
   - Data type (SQL type code: C, D, I, T, etc.)
   - Length / precision
   - Scale (for numeric types)
   - Null allowance (Y/N)
   - Default value (if present)
   - Comments or COLTEXT (if present)

3. **Constraint Evidence**:
   - Primary key: list columns and order from approved QSYS2 catalog extract or DDL
   - Unique constraints: list columns and order
   - Foreign keys: source and target table/column pairs
   - Check constraints: constraint expression (rare)

4. **Index Evidence**:
   - Index name
   - Columns and order
   - Uniqueness (UNIQUE or non-unique)
   - Filtered (WHERE clause, if present)

## Common DB2 on IBM i Patterns

### Pattern: System-Managed Identity Column

```sql
CREATE TABLE ORDERS (
    ORDER_ID INTEGER GENERATED ALWAYS AS IDENTITY,
    CUSTNO CHARACTER(10),
    ORDDATE DATE,
    PRIMARY KEY (ORDER_ID)
);
```

**Interpretation**: ORDER_ID is auto-generated by DB2; not supplied by application.

### Pattern: Timestamp Columns

```sql
CREATE TABLE CUSTOMER (
    CUSTNO CHARACTER(10) PRIMARY KEY,
    CUSTNAME CHARACTER(30),
    CREATED_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

**Interpretation**: CREATED_TS set once on insert; UPDATED_TS updated on each modify.

### Pattern: Referential Integrity

```sql
ALTER TABLE ORDER ADD CONSTRAINT FK_ORD_CUST
    FOREIGN KEY (CUSTNO) REFERENCES CUSTOMER (CUSTNO)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT;
```

**Interpretation**: ORDER rows cannot reference non-existent CUSTOMER; cannot delete CUSTOMER while ORDER rows exist.

---

Generated by legacy-ibmi-data-model-analyzer v0.1.0
Legacy Spec Factory Copyright 2026 Leo L Zhang
