

def add_clusters_pageRank_Database(driver, agent_nodes):
    with driver.session() as session:
        print("Removing nodes with 0 interactions")
        # Remove nodes with no interactions
        session.run("""
            MATCH (n)
            WHERE size((n)--())=0
            DELETE (n)
            """)
        
        print("Add topics to the Agents")
        session.run("""
            match (i:Agent)-[:TOPIC]->(k:Keyword)
            with i, collect(k.edam) as cedam, collect(k.label) as clabel
            set i.topiclabel=clabel
            set i.topicedam =cedam
            return distinct *
            """)
        
        print("Add TypeAgent to the Agents")
        session.run("""
            match (i:Agent)-[:HAS_TYPE]->(k:TypeAgent)
            with i, collect(k.name) as cname
            set i.agentType=cname
            return distinct *
            """)
        
        print("Add Databases nodes")
        session.run("""
            match (i:Agent)
            where "db" in i.agentType
            WITH collect(i) AS databases
            CALL apoc.refactor.rename.label("Agent", "Database", databases)
            YIELD committedOperations
            RETURN committedOperations
            """)
        # Remove previous nodes and edges
        session.run("""MATCH ()-[r:METAOCCUR_COMM]->() DELETE r""")
        session.run("""MATCH ()-[r:HAS_COMMUNITY]->() DELETE r""")
        session.run("""MATCH (r:Community) DELETE r""")
        
        print("Creating view")
        ### PageRank
        # Create view with the property
        session.run("""
            CALL gds.graph.create(
            'got-weighted-interactions',
            ['Agent', 'Publication', 'Database'],
            {
                METAOCCUR_ALL: {
                    orientation: 'UNDIRECTED',
                    aggregation: 'NONE',
                    properties: {
                        times: {
                        property: 'times',
                        aggregation: 'NONE',
                        defaultValue: 0.0
                        }
                    }
                }
            }
            )
            """)
        print("PageRank")
        # Write PageRank values to each node
        session.run("""
            CALL gds.pageRank.write(
                'got-weighted-interactions', 
                {
                    relationshipWeightProperty: 'times',
                    writeProperty: 'pageRank'
                }
            )
            """)
        print("Louvain")
        # Write the community id to each node
        session.run("""
            CALL gds.louvain.write(
                'got-weighted-interactions',
                {
                    relationshipWeightProperty: 'times',
                    writeProperty: 'community'
                }
            )
            """)

        print("Create clusters for all dataset")
        # Create clusters as nodes
        session.run("""
            MATCH (n) 
            WITH distinct n.community as com
            CREATE (:Community {com_id: com})
            """)
        # Edges between nodes and its communities
        session.run("""
            MATCH (n),(i:Community) 
            WHERE n.community = i.com_id
            CREATE (n)-[:HAS_COMMUNITY]->(i)
            """)
        session.run("""
            MATCH (c2:Community)<-[h2:HAS_COMMUNITY]-(p)-[m:METAOCCUR_ALL]-(n)-[h:HAS_COMMUNITY]->(c1:Community)
            WHERE c1<> c2
            WITH c2,c1, collect(m) as co
                UNWIND co as c 
            WITH c2, sum(c.times) as sumo , c1
            CREATE (c1)-[:METAOCCUR_COMM {times: sumo}]->(c2)
            """)
        # Delete duplicated and reversed relationships
        session.run("""
            Match (c1:Community)-[r:METAOCCUR_COMM]->(c2:Community)
            where c1.com_id < c2.com_id
            delete r
            """)

        #################### Create community properties #######################
        
        print("Creating community properties")
        ### Add most common topics in the communities
        # Empty topic for all the communities
        session.run("""
            MATCH (n:Community)
            set n.mtopic=NULL, n.ctopic=NULL
            return n.mtopic,n.ctopic
            """)
        # Topics for communities bigger than 1
        session.run("""
            Match (l:Keyword)<-[:TOPIC]-(i)-[:HAS_COMMUNITY]->(c)
            with c,l,count(i) as counti
            order by counti DESC
            with c,collect(l)[0] as mtopic, max(counti) as maxcount
            set c.mtopic=mtopic.label, c.ctopic=id(mtopic)
            return c,mtopic, maxcount
            """)
        ### Add most common languages in the communities
        # Empty language for all the communities
        session.run("""
            MATCH (n:Community)
            set n.mlanguage=NULL, n.clanguage=NULL
            return n.mtopic,n.ctopic
            """)
        # Languages for communities bigger than 1
        session.run("""
            Match (l:Language)<-[:USE_LANGUAGE]-(i)-[:HAS_COMMUNITY]->(c)
            with c,l,count(i) as counti
            order by counti DESC
            with c,collect(l)[0] as mlanguage, max(counti) as maxcount
            set c.mlanguage=mlanguage.name, c.clanguage=id(mlanguage)
            return c,mlanguage, maxcount
            """)
        ### Add most common Operative system in the community
        # Empty OS for all the communities
        session.run("""
            MATCH (n:Community)
            set n.mos=NULL, n.cos=NULL
            return n.mtopic,n.ctopic
            """)
        # OS for communities bigger than 1
        session.run("""
            Match (l:OS)<-[:USE_OS]-(i)-[:HAS_COMMUNITY]->(c)
            with c,l,count(i) as counti
            order by counti DESC
            with c,collect(l)[0] as mlanguage, max(counti) as maxcount
            set c.mos=mlanguage.name, c.cos=id(mlanguage)
            return c,mlanguage, maxcount
            """)
    
        #Remove previous graphs
        session.run("""
            CALL gds.graph.drop('got-weighted-interactions')
        """)
