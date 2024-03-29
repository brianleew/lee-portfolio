# Demand Response Portal Database Documentation (v5.1)

Welcome to the comprehensive documentation for the Demand Response Portal (DRP) database schema. This documentation provides an in-depth exploration of the schema's structure, tables, relationships, and key features. The DRP database schema has been meticulously designed to effectively manage data related to users, organizations, meters, and meter data, facilitating a seamless data resource management experience within the context of demand response initiatives.

### **Purpose and Overview**

The DRP database schema serves as the foundational structure supporting the Demand Response Portal. It ensures the organization, accessibility, and integrity of data crucial for data visualizations and portal access. By adhering to established database design principles and normalization, the DRP team have created a simple yet robust schema to meet the needs of the application.

### **Table of Contents**

This documentation is organized as follows:

1. **Introduction:** A high-level overview of the schema's purpose, its role within demand response, and the key objectives it aims to fulfill.
2. **Tables and Relationships:** Detailed insights into each table, its attributes, primary and foreign keys, and relationships with other tables as well as the supporting triggers.
3. **Data Workflow:** Descriptions of how data flows through the schema, including account creation and management, access control strategies, and meter data insertion.
4. **API:** [WIP]

### **Getting Started**

Whether you're a developer, administrator, or stakeholder involved in the demand response project, this documentation will provide valuable insights into the database schema's structure and functionalities, contextualized for the complexities of the demand response portal. By understanding how the schema aligns with demand response portal objectives, you'll be better equipped to make informed decisions and contribute to successful demand response programs.

We encourage you to navigate through the sections that align with your interests and responsibilities within the demand response context.

**[Schema Design](https://drawsql.app/teams/drp-1/diagrams/drp/embed)**

# Introduction:

The Demand Response Portal (DRP) database serves as the backbone for managing user interactions and meter data. It provides the necessary data to support both residential and organization accounts. By seamlessly integrating user account management, meter usage tracking, and organization affiliations, the DRP database ensures efficient data organization and retrieval.

### Residential and Organization Account Support

The DRP schema accommodates both residential as well as industrial/commercial customers. For residential users, it allows for account creation of individual accounts linked to their respective meter, ensuring accurate monitoring of energy usage. Industrial and commercial customers are able to establish organization accounts that allow oversight of all meters and users in their organization.

### User Management

The **users** table captures essential user details, including email, name, and any affiliations. The **approval_status** field enables controlled onboarding, ensuring that only approved accounts gain access to the system.

### Secure Authentication

The **login** table safeguards user authentication through the storage of hashed passwords alongside the appropriate **account_id**. This security ensures the user credentials are protected, maintaining the integrity of the portal and safeguarding user data.

### Flexible Meter Mapping

The **meter_map**  table offers a flexible approach to associating users and organizations with meters. With the **entity_id** that can refer to either a **account_id** for residential users or an **org_id** industrial/commercial users, the schema provides a dynamic means of tracking meter ownership and usage across the residential and organizational spectrum.

# Tables and Relationships

This section will dive deeper into the tables and their relationships. It will include table specific details such as fields, primary keys, and types. It will also include details about the relationships between the tables including the triggers and foreign keys used to enforce data integrity in the schema.

## Entities

### Layout
| entity_id |           entity_type           |
|-----------|---------------------------------|
| int       | enum [ 'user', 'organization' ] |

### Fields
**entity_id**

**entity_type**

## Users

### Layout
| account_id | email        | first_name  | last_name   | org_id | approval_status                                    |
|------------|--------------|-------------|-------------|--------|----------------------------------------------------|
| int        | varchar(254) | varchar(50) | varchar(50) | int    | enum [ 'Pending', 'Approved', 'Rejected', 'Admin'] |

### Fields

### Triggers


## Organizations

### Layout
| org_id | org_name    | coordinates |
|--------|-------------|-------------|
| int    | varchar(50) | point       |

### Fields

### Triggers


## Logins

### Layout
| account_id | password_hash |
|------------|---------------|
| int        | varchar(64)   |

### Fields


## Sessions

### Layout
| session_id | account_id | session_expire |
|------------|------------|----------------|
| uuid       | int        | datetime       |

### Fields


## Meters

### Layout
| meter_id | coordinates |
|----------|-------------|
| int      | point       |

### Fields

### Triggers


## Meter Map

### Layout
| entity_id | meter_id |
|-----------|----------|
| int       | int      |

### Fields

### Triggers


## Meter Data

### Layout
| meter_id | start_time | end_time | meter_value  | prediction_value | delta_value  |
|----------|------------|----------|--------------|------------------|--------------|
| int      | datetime   | datetime | decimal(8,2) | decimal(8,2)     | decimal(8,2) |

### Fields

### Triggers


## DRP Periods

### Layout
| drp_id | start_time | end_time |
|--------|------------|----------|
| int    | datetime   | datetime |

### Fields

### Triggers