

def create_SQL_tables(c):
        
    # Create Publications table - It will be used to create Publication nodes
    # id: Primary key of the publication
    # title: Title of the publication
    # year: Year of the publication
    # pmid: PMID of the publication
    # doi: DOI of the publication
    c.execute('''DROP TABLE IF EXISTS Publications''')
    c.execute('''CREATE TABLE IF NOT EXISTS "Publications" (
                    "title"	TEXT NOT NULL,
                    "year" INTEGER,
                    "pmid" INTEGER NOT NULL,
                    "doi" TEXT UNIQUE,
                    PRIMARY KEY("pmid")
                );''')

    # Create Citations table - It will be used to create Publication-Publication edges
    # id1: Foreign key of publication
    # id2: Foreign key of the second publication
    # n_citations: Number of co-occurences between publications
    # year: Year when the co-occurence happenend.
    c.execute('''DROP TABLE IF EXISTS Citations''')
    c.execute('''CREATE TABLE "Citations" (
                    "id1"	TEXT NOT NULL,
                    "id2"	TEXT NOT NULL,
                    "n_citations" INTEGER,
                    "year" INTEGER
                );''')

    c.execute('''DROP TABLE IF EXISTS Citations_backup''')

    #Create Agents table - It will be used to create Agent nodes
    #name: Name of the InferedAgent
    c.execute('''DROP TABLE IF EXISTS Agents''')
    c.execute('''CREATE TABLE IF NOT EXISTS "Agents" (
                    "name" TEXT NOT NULL,
                    "label" TEXT,
                    PRIMARY KEY("label")
                )''')
    
    #Create Languages table - Table storing all the programming languages of the agents
    #Language: Name of the programming language
    c.execute('''DROP TABLE IF EXISTS TypeAgent''')
    c.execute('''CREATE TABLE IF NOT EXISTS "TypeAgent" (
                    "Type" TEXT NOT NULL,
                    PRIMARY KEY("Type")
                )''')

    #Table for the relationships between the agents and its programming languages
    #Language: Name of the programming language
    #label: Name of the agent
    c.execute('''DROP TABLE IF EXISTS AgentsToTypeAgent''')
    c.execute('''CREATE TABLE IF NOT EXISTS "AgentsToTypeAgent" (
                    "Type" TEXT NOT NULL,
                    "label" TEXT NOT NULL,
                    UNIQUE(Type, label), 
                    FOREIGN KEY("Type") REFERENCES "TypeAgent"("Type"),
                    FOREIGN KEY("label") REFERENCES "Agents"("label")
                )''')

    #Create Languages table - Table storing all the programming languages of the agents
    #Language: Name of the programming language
    c.execute('''DROP TABLE IF EXISTS Languages''')
    c.execute('''CREATE TABLE IF NOT EXISTS "Languages" (
                    "Language" TEXT NOT NULL,
                    PRIMARY KEY("Language")
                )''')

    #Table for the relationships between the agents and its programming languages
    #Language: Name of the programming language
    #label: Name of the agent
    c.execute('''DROP TABLE IF EXISTS AgentsToLanguages''')
    c.execute('''CREATE TABLE IF NOT EXISTS "AgentsToLanguages" (
                    "Language" TEXT NOT NULL,
                    "label" TEXT NOT NULL,
                    UNIQUE(Language, label), 
                    FOREIGN KEY("Language") REFERENCES "Languages"("Language"),
                    FOREIGN KEY("label") REFERENCES "Agents"("label")
                )''')

    #Create Operative systems table - Table storing all the operative systems of the agents
    #name: Name of the operative system
    c.execute('''DROP TABLE IF EXISTS OperativeSystems''')
    c.execute('''CREATE TABLE IF NOT EXISTS "OperativeSystems" (
                    "name" TEXT NOT NULL,
                    PRIMARY KEY("name")
                )''')

    #Table for the relationships between the agents and its operative systems
    #os: Name of the operative system
    #label: Name of the agent
    c.execute('''DROP TABLE IF EXISTS AgentsToOS''')
    c.execute('''CREATE TABLE IF NOT EXISTS "AgentsToOS" (
                    "os" TEXT NOT NULL,
                    "label" TEXT NOT NULL,
                    UNIQUE(os, label),
                    FOREIGN KEY("label") REFERENCES "Agents"("label")
                )''')

    #Create InferedAgents-Publications table - It will be used to connect the agents and the publications that describe the agent
    #label: Name of InferedAgent node.
    #Publication_id: Id of a Publication.
    c.execute('''DROP TABLE IF EXISTS AgentsToPublications''')
    c.execute('''CREATE TABLE IF NOT EXISTS "AgentsToPublications" (
                    "label" TEXT NOT NULL,
                    "Publication_id" TEXT NOT NULL,
                    FOREIGN KEY("label") REFERENCES "Agents"("label"),
                    FOREIGN KEY("Publication_id") REFERENCES "Publications"("id")
                )''')

    #Create Keywords table - It is used to store all the EDAM ontology terms of the database
    #edam_id: Identifier of the EDAM
    #readableID: Human readable label of the EDAM id
    c.execute('''DROP TABLE IF EXISTS Keywords''')
    c.execute('''CREATE TABLE IF NOT EXISTS "Keywords" (
                    "edam_id" TEXT NOT NULL,
                    "readableID" TEXT NOT NULL,
                    PRIMARY KEY("edam_id")
                )''')

    list_edam_relationships = ["InputData", "InputFormat",
                            "OutputData", "OutputFormat",
                            "Topics", "Operations"]
    for edam_term in list_edam_relationships:
        
        #Create InferedAgents-keywords table - It will be used to relate the EDAM terms and the agents
        #label: Name of the InferedAgent
        #Keyword: Name of the EDAM keyword
        c.execute(f'''DROP TABLE IF EXISTS {edam_term}''')
        c.execute(f'''CREATE TABLE IF NOT EXISTS "{edam_term}" (
                        "label" TEXT NOT NULL,
                        "keyword" TEXT,
                        UNIQUE(label, keyword), 
                        FOREIGN KEY("label") REFERENCES "InferedAgents"("label"),
                        FOREIGN KEY("keyword") REFERENCES "Keywords"("edam_id")
                    )''')
        
    c.execute('''DROP TABLE IF EXISTS SubclassEDAM''')
    c.execute('''CREATE TABLE IF NOT EXISTS "SubclassEDAM" (
                    "edam_id" TEXT,
                    "subclass_edam" TEXT,
                    "subclass_type" TEXT,
                    UNIQUE(edam_id, subclass_edam)                
                )''')




