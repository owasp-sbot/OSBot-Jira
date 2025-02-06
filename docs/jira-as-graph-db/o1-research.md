# Using Jira as a Graph-Like Database

Jira is primarily an issue and project tracking tool, but its flexible issue linking system allows it to represent graph-like data. In this model, **each Jira issue can act as a node**, and **issue links serve as edges** connecting these nodes. This sectioned report explores how to implement and leverage graph structures in Jira, best practices for modeling such data, the benefits and challenges of using Jira in this way, and tools or alternatives to enhance Jira’s graph capabilities.

## Graph Relationships via Jira Issues and Links

### Issue Linking in Jira

Jira allows linking any two issues to indicate a relationship. A link in Jira is essentially **an association between two issues** (or between an issue and another resource like a Confluence page or external URL). Each link has a *type* (e.g., “relates to”, “blocks”, “duplicates”) with an *outward* and *inward* description to express directed semantics (for example, *“Issue A blocks Issue B”* vs *“Issue B is blocked by Issue A”*). These link types do **not impose any behavior** beyond labeling the relationship – they are essentially markers to inform users of how two issues are related. Because links are arbitrary and not confined to a strict hierarchy, you can form complex networks of issues.

### Nodes and Edges

With this mechanism, **Jira issues become the nodes of a graph, and issue links are the edges** connecting them. For example, you might create issues that represent entities (like components, requirements, people, etc.) and use links to represent relationships between them (such as dependencies, associations, ownership, etc.). Jira’s linking is many-to-many – any issue can link to any other – which means you can model arbitrary graph structures (not just trees). Even Jira’s built-in hierarchy (Epics and sub-tasks) can be seen as specialized links (Epic links, parent/sub-task relationships), though the general issue linking feature is more flexible for graph modeling.

### Visualizing the Graph

Out of the box, when you view a Jira issue you will see a list of all issues directly linked to it (one hop away). This provides a local view of the graph around a node. However, Jira does not natively show a full network graph of all connected issues. Users have long desired a “link map” to visualize the whole network of issue relationships. In practice, teams often use plugins or external tools to visualize the issue graph. Several Jira add-ons (e.g., *Link Hierarchy*, *Issue Links Viewer*, *Pathfinder*) specifically render a **graph view where nodes are issues and edges are the links** between them. This confirms that Jira’s data can indeed be interpreted as a graph and visualized for better understanding of relationships.

## Implementation and Modeling in Jira

Using Jira to store graph-like data involves configuring your issues and links to represent the nodes and edges of your domain. Here are some best practices for implementing this:

### Define Node Types with Issue Types

- Use Jira **Issue Types** (or labels/projects) to distinguish different node categories.
- Example: A knowledge graph may use “Concept” and “Resource” issue types, linking them to represent relationships.

### Use Link Types to Encode Relationships

- Leverage Jira’s customizable **issue link types** to label different kinds of edges.
- Example: Use “blocks” for dependencies, “causes” for impact relationships, and “relates to” for loose associations.
- Meaningful link types ensure clarity and consistency in the graph model.

### Storing Properties

- Node properties are stored as issue custom fields.
- Edge properties are more limited, as Jira issue links do not have custom fields.
- Workaround: Store relationship details in comments or descriptions.

### Organizing Projects for the Graph

- Separate node categories by **Jira project**, **components**, or **labels** to maintain clarity.
- Example: One project for “Risks” and another for “Controls,” with links denoting mitigations.

### Maintain Link Discipline

- Establish guidelines for linking, ensuring meaningful relationships.
- Remove redundant or outdated links to keep the graph clean.
- Document the schema of your graph (node types and link types) for team reference.

### Example: Modeling Dependencies

- Each issue (Story, Task, etc.) is a node.
- Use the “blocks” link type to model dependencies (A "blocks" B when A must be completed before B).
- This creates a **directed acyclic graph (DAG)** of work dependencies.

## Benefits of Modeling Graph Data in Jira

### Leverage Familiar Interface

- Users can interact with nodes (issues) through the Jira interface.
- Each issue’s detail view shows its direct connections, improving understanding.

### Built-in Metadata and Workflow

- Each issue (node) supports metadata (status, priority, custom fields, etc.).
- Issues can go through Jira’s workflow, adding process control.

### Traceability and Dependency Tracking

- Links support **traceability matrices** (e.g., linking requirements to test cases for validation).
- Queries (JQL) can filter issues by link type (e.g., "find all issues linked to X").

### Unified Source of Truth

- Jira acts as a **lightweight knowledge graph** for organizations, connecting related information.
- Integration with Confluence allows linking Jira issues to documentation.

### Ecosystem and Integrations

- Many marketplace apps exist to **extract or visualize graph data**.
- The Jira REST API enables external analysis or visualization (e.g., exporting to Neo4j).

## Challenges and Limitations

### No Multi-Hop View or Query by Default

- Jira’s UI only displays immediate links.
- JQL does not support recursive queries.
- No built-in graph traversal functionality.

### Performance and Scale

- Jira uses a **relational database**, not optimized for large-scale graph traversal.
- Large graphs (thousands of issues) can slow down UI interactions.

### Limited Link Metadata and Constraints

- Links cannot store additional properties beyond type.
- No built-in validation for preventing cycles or enforcing link constraints.

### Visualization and Usability

- Jira lacks **graph visualization out of the box**.
- Navigating deep issue relationships requires **third-party plugins**.

### Lack of Graph Query Language

- No built-in Cypher or SPARQL-like querying.
- GraphQL support is limited.
- Workaround: Use scripts to traverse relationships via REST API.

## Tools and Integrations

### Visualization Plugins

- *Issue Links Viewer*, *STAGIL Issue Maps*, *Pathfinder* – Graph visualization tools for Jira.
- Provide **interactive graphs of linked issues**.

### Planning and Dependency Management

- *BigPicture*, *Advanced Roadmaps* – Focused on dependencies and project planning.
- Useful for visualizing **dependency networks**.

### Integration with Graph Databases

- Export Jira issues and links to **Neo4j** for advanced graph queries.
- Example: Use **jQAssistant** to sync Jira data with Neo4j.

## Conclusion

Jira’s issue linking system provides a **flexible foundation** for representing graph data. While it has limitations compared to dedicated graph databases, its ecosystem of **plugins and integrations** helps overcome these gaps. **Teams can model knowledge graphs, dependency networks, and traceability matrices within Jira**, but for deep graph analytics, external tools like **Neo4j** may be necessary. Combining Jira’s usability with graph processing capabilities can yield powerful results.

<br/>
<br/>
<br/>
<br/>

----------

----------

# Appendix: Raw o1 Deep Research result (with links)

--------

# Using Jira as a Graph-Like Database

Jira is primarily an issue and project tracking tool, but its flexible issue linking system allows it to represent graph-like data. In this model, **each Jira issue can act as a node**, and **issue links serve as edges** connecting these nodes ([
	Solved: Visual overview of related and blocked issues?
](https://community.atlassian.com/t5/Jira-questions/Visual-overview-of-related-and-blocked-issues/qaq-p/757970#:~:text=Although%20I%20am%20not%20particularly,and%20the%20link%20between%20those))  This sectioned report explores how to implement and leverage graph structures in Jira, best practices for modeling such data, the benefits and challenges of using Jira in this way, and tools or alternatives to enhance Jira’s graph capabilities.

## Graph Relationships via Jira Issues and Links

**Issue Linking in Jira:** Jira allows linking any two issues to indicate a relationship. A link in Jira is essentially **an association between two issues** (or between an issue and another resource like a Confluence page or external URL) ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=First%20of%20all%2C%20what%20are,showing%20dependencies%20between%20different%20issues))  Each link has a *type* (e.g. “relates to”, “blocks”, “duplicates”) with an *outward* and *inward* description to express directed semantics (for example, *“Issue A blocks Issue B”* vs *“Issue B is blocked by Issue A”*) ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=,an%20issue%C2%A0is%20affected%C2%A0by%20another%20issue))  These link types do **not impose any behavior** beyond labeling the relationship – they are essentially markers to inform users of how two issues are related ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=Does%20Outward%20or%20Inward%20Description,more%20on%20this%20later))  Because links are arbitrary and not confined to a strict hierarchy, you can form complex networks of issues.

**Nodes and Edges:** With this mechanism, **Jira issues become the nodes of a graph, and issue links are the edges** connecting them ([Issue Graph | Atlassian Marketplace](https://marketplace.atlassian.com/apps/1213005/issue-graph#:~:text=,projects%20or%20particular%20issue%20types))  ([
	Solved: Visual overview of related and blocked issues?
](https://community.atlassian.com/t5/Jira-questions/Visual-overview-of-related-and-blocked-issues/qaq-p/757970#:~:text=Although%20I%20am%20not%20particularly,and%20the%20link%20between%20those))  For example, you might create issues that represent entities (like components, requirements, people, etc.) and use links to represent relationships between them (such as dependencies, associations, ownership, etc.). Jira’s linking is many-to-many – any issue can link to any other – which means you can model arbitrary graph structures (not just trees). Even Jira’s built-in hierarchy (Epics and sub-tasks) can be seen as specialized links (Epic links, parent/sub-task relationships), though the general issue linking feature is more flexible for graph modeling.

**Visualizing the Graph:** Out of the box, when you view a Jira issue you will see a list of all issues directly linked to it (one hop away). This provides a local view of the graph around a node. However, Jira does not natively show a full network graph of all connected issues. Users have long desired a “link map” to visualize the whole network of issue relationships ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=When%20viewing%20an%20issue%20you,node%20%28or%20link%29%20away))  ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=A%20,in%20a%20given%20project))  In practice, teams often use plugins or external tools to visualize the issue graph. Several Jira add-ons (e.g. *Link Hierarchy*, *Issue Links Viewer*, *Pathfinder*) specifically render a **graph view where nodes are issues and edges are the links** between them ([
	Solved: Visual overview of related and blocked issues?
](https://community.atlassian.com/t5/Jira-questions/Visual-overview-of-related-and-blocked-issues/qaq-p/757970#:~:text=Although%20I%20am%20not%20particularly,and%20the%20link%20between%20those))  This confirms that Jira’s data can indeed be interpreted as a graph and visualized for better understanding of relationships.

## Implementation and Modeling in Jira

Using Jira to store graph-like data involves configuring your issues and links to represent the nodes and edges of your domain. Here are some best practices for implementing this:

- **Define Node Types with Issue Types:** Determine what each node in your graph represents and use Jira **Issue Types** (or labels/projects) to distinguish them. For example, in a knowledge graph you might use a custom issue type “Concept” for concept nodes and another type “Resource” for resource nodes, linking them to represent relationships. The flexibility of Jira issues means each “node” can carry attributes in its fields (text, select lists, etc.), attachments, and even workflows if needed.

- **Use Link Types to Encode Relationships:** Leverage Jira’s customizable **issue link types** to label different kinds of edges. Jira comes with a few default link types (“Relates”, “Blocks”, “Duplicate”, “Cloners”), but admins can add custom link types to fit your model ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=Does%20Outward%20or%20Inward%20Description,more%20on%20this%20later))  ([Best Practices for Organizing a Jira Issue - Stiltsoft](https://stiltsoft.com/blog/best-practices-for-organizing-a-jira-issue/#:~:text=Issue%20linking%20allows%20you%20to,For%20example))  For example, you could add link types like “depends on”, “causes”, “parent of” etc., each with appropriate inward/outward descriptions. Using meaningful link types is important for clarity – it’s essentially your graph’s edge labels. It’s a best practice to use “Blocks” or similar for true dependency relationships and reserve “Relates” for loose associations ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=As%20you%20might%20have%20noticed%2C,more%20useful%20for%20technical%20associations))  whereas duplicate/cloner links might indicate same or copied items. Consistently using link types will make the graph semantics clear to users.

- **Storing Properties:** In graph databases, edges and nodes can have properties. In Jira, node properties are just custom fields on issues – you have a rich set of field types to store metadata on each issue (node). Edge properties are more limited since Jira’s issue links don’t have fields of their own (a link is not a first-class entity you can annotate beyond its type). If you need to record details about a relationship, one workaround is to capture it in the description or comments of the linked issues (e.g., mention why two nodes are linked). In extreme cases, some teams represent an edge as its own issue (e.g. an “Relationship” issue that links to the two endpoint issues), but that complicates the model. Generally, try to encode all necessary relationship info either in the link type or in the node fields.

- **Organize Projects for the Graph:** If your graph nodes fall into distinctly different categories, you might separate them by Jira project or by components/labels within a project. This isn’t strictly necessary, but it can help partition the data. For instance, one real-world usage had a project for “Risks” and another for “Controls” and linked issues across projects to show which risks were mitigated by which controls. Jira supports links across projects seamlessly ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=First%20of%20all%2C%20what%20are,showing%20dependencies%20between%20different%20issues))  Organizing this way can also help apply different workflows or permissions to different node types (e.g., if some nodes represent tasks that need to be completed, they might be in a project with a workflow, whereas conceptual nodes might be in a project with a simpler workflow).

- **Maintain Link Discipline:** As with any graph, a Jira-based graph can become chaotic if over-linked. It’s wise to establish guidelines on what types of issues should be linked, and how. Avoid creating links that don’t have a clear meaning. If a particular relationship is no longer relevant, remove the link to keep the data clean. Remember that **Jira links are just associations and do not enforce any rules** ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=First%20of%20all%2C%20what%20are,One)) – so it’s up to your process to ensure the links (edges) remain meaningful. Document the schema of your graph (what the node types are and what each link type denotes) so team members use it consistently.

- **Example – Modeling Dependencies:** A common graph use-case in Jira is modeling task dependencies (a prerequisite graph of issues). In this case, each issue (Story, Task, etc.) is a node, and you would use the “blocks / is blocked by” link type to denote dependency edges. The recommendation is to link Issue A “blocks” Issue B when A must be done before B ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=%5BImage%203%3A%20Jira))  This effectively creates a directed acyclic graph of work dependencies. Jira will list “blocks” links on each issue, but you might need an add-on to visualize the full dependency network or to do multi-step analysis (see **Challenges** below). Another example: modeling a knowledge graph – you might have issues for “Term” and link them with a custom “related to” link to build an ontology network.

By structuring issue types and link types upfront, Jira can store a surprisingly complex graph of information. The data remains accessible via Jira’s UI (each issue shows its immediate connections) and via the API for more global analysis. An organization that did this, for instance, was able to claim **“We use Jira as a Graph Database”** for tracking security issues, treating issue fields as node attributes and links (including Epic links) as relationships in a security knowledge graph ([Thinking in graphs v1.0 | PPT](https://www.slideshare.net/slideshow/thinking-in-graphs-v10/101283923#:~:text=,)) 

## Benefits of Modeling Graph Data in Jira

Using Jira to represent graph-like relationships comes with several advantages:

- **Leverage Familiar Interface:** Users interact with nodes (issues) through the same Jira interface they use for other work. This means they can create, edit, and link nodes without learning a new system. Each issue’s detail view shows its links, providing context about related nodes. This can improve understanding of how pieces of a project or knowledge base interconnect. For example, linking related issues makes a project **much more organized** – everyone can easily see associations that might not be obvious from just text, ensuring that dependencies or related work aren’t overlooked ([Best Practices for Organizing a Jira Issue - Stiltsoft](https://stiltsoft.com/blog/best-practices-for-organizing-a-jira-issue/#:~:text=Your%20projects%20will%20look%20much,while%20browsing%20across%20the%20project))  ([Best Practices for Organizing a Jira Issue - Stiltsoft](https://stiltsoft.com/blog/best-practices-for-organizing-a-jira-issue/#:~:text=Issue%20linking%20allows%20you%20to,For%20example)) 

- **Built-in Metadata and Workflow:** Each issue (node) can have rich metadata (status, priority, custom fields, etc.) and even go through Jira’s workflow. This is something a plain graph database won’t provide out-of-the-box. For instance, if nodes represent tasks or requirements, they can still have statuses (Open, In Progress, Done) and assignees, so you get the benefit of project tracking on your graph nodes. Jira’s permissions and notifications also apply, which can be useful if certain relationships should trigger updates or if certain nodes should only be visible to certain teams.

- **Traceability and Dependency Tracking:** Once links are in place, Jira’s queries (JQL) and reports can be used (to a limited extent) to track dependencies or impact. You can filter issues “linked to” a certain critical item, or see all issues of a type that are blocking others. This is helpful for **traceability** in areas like requirements engineering and testing: e.g., you link a Requirement issue to the related User Stories implementing it, and further to Test cases – forming a chain. Teams do use Jira to maintain such traceability matrices and benefit by having all this data in one system rather than scattered ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=Jira%20currently%20has%20the%20ability,Blocker%2C%20Reference%2C))  ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=A%20,in%20a%20given%20project))  The presence of links can be used as a check (for example, finding requirements with no linked tests, indicating a coverage gap).

- **Unified Source of Truth:** Storing graph data in Jira means it resides alongside your project tasks or knowledge base in one system. There’s no need to sync data between a separate graph database and your issue tracker; the issues themselves carry the relationships. This can reduce tooling complexity. Project leads have a single place to go to understand the “big picture” – with the aid of visualizations or queries, Jira can provide a **map of all related issues** in a project, giving better understanding of the overall structure and dependencies ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=A%20,in%20a%20given%20project))  In essence, Jira can serve as a lightweight knowledge graph for your organization, tying together disparate pieces of information (tasks, requirements, incidents, components, etc.) via links.

- **Ecosystem and Integrations:** Because Jira is widely used, many tools and plugins exist to extract or visualize data. If you use Jira as your graph store, you can tap into numerous apps (or the REST API) to build custom reports, charts, or export data. We’ll discuss specific tools in the next section, but it’s a benefit that you can later enhance your graph with off-the-shelf solutions (for example, visualize it with a marketplace app or analyze it with an external script) without having to migrate data from another system.

In summary, the main benefit is **convenience** – you’re repurposing Jira’s robust issue tracking capabilities to manage graph-structured data, which can be especially handy if the data naturally ties into your projects. Teams have found that visualizing issue links as a graph gives a much clearer understanding of complex dependencies within Jira ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=A%20,in%20a%20given%20project))  all while keeping data within the familiar Jira environment.

## Challenges and Limitations of Jira as a Graph Database

While Jira can store nodes and edges, it is **not a true graph database**, and there are important limitations to be aware of:

- **No Multi-Hop View or Query by Default:** Jira’s UI only shows immediate links on an issue page – you can’t natively see a full network graph or traverse multiple hops in one view. As one Atlassian suggestion lamented, *“When viewing an issue you can see the 'links' of all issues that are 1-node away. What is missing is the whole picture.”* ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=When%20viewing%20an%20issue%20you,node%20%28or%20link%29%20away))  There’s no built-in feature to interactively explore the web of linked issues beyond one level. Similarly, **JQL (Jira’s query language) has limited support for graph queries**. You can query for issues linked to a specific issue or of a certain link type (using functions like `linkedIssues()`), but you cannot easily query, say, “all issues linked to issues that are linked to X” in a single step, nor can you do arbitrary path searches. Users have requested features to filter issues and their dependents over multiple projects, but Atlassian did not implement these in core Jira ([Loading...](https://jira.atlassian.com/browse/JRACLOUD-35383#:~:text=could%20you%20please%20allow%20filtering,on%2C%20also%20over%20multiple%20projects)) 

- **Performance and Scale:** Jira’s underlying database is relational and not optimized for graph traversal. If you create extremely large graphs (thousands of interlinked issues), certain operations may become slow or unwieldy. For example, an issue with hundreds of links might load slowly in the UI, and finding paths between two distant nodes would require many API calls or expensive queries. Jira doesn’t index transitive relationships, so analyzing the graph deeply means pulling a lot of data into memory or an external tool. In short, **Jira can handle many issues and links, but it cannot perform graph algorithms (like shortest path, centrality, etc.) natively**. That kind of analysis would need to be offloaded to a dedicated graph engine.

- **Limited Link Metadata and Constraints:** As mentioned, Jira’s issue links are simple: just a connection with a type. You cannot attach additional properties to a link (no weight, date, or custom attribute on the relationship itself, aside from an optional link comment which is just an unstructured note). This is a stark difference from graph databases where relationships can hold rich data. Also, Jira does not enforce referential integrity beyond existence – there’s nothing preventing creating contradictory or circular links unless you build a custom validator. For example, Jira will happily let you create a cycle in a dependency graph (Issue A blocks B, B blocks C, C blocks A) even though that might not make logical sense; it’s on users or plugins to catch such scenarios. Jira also will not automatically update anything based on link changes (aside from maybe triggering some add-on behaviors). **In short, the semantics of the graph are entirely up to how you use it**, with no enforcement from Jira beyond basic link type definitions ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=First%20of%20all%2C%20what%20are,One)) 

- **Visualization and Usability:** Without additional tools, it can be difficult for users to understand the graph stored in Jira. A list of links on each issue is useful, but for complex webs, users benefit from a visual graph or at least a tree view. Jira does not provide this visualization out-of-the-box. This is why many rely on plugins or export data to graph visualization tools. Additionally, navigating the graph in Jira can be cumbersome – you have to click through issues to follow a chain. There is no “graph explorer” UI in Jira Software. This lack can reduce the accessibility of the information, making it harder to see the big picture or to follow long chains of relationships without custom solutions.

- **Lack of Graph Query Language:** Jira’s REST API allows you to fetch an issue’s links easily, but if you wanted to query the graph in a more complex way (e.g., “find all nodes connected within 3 hops to X that meet certain criteria”), you would need to write a script to perform iterative queries. Atlassian has been working on a GraphQL API for their platform, which in theory could allow more efficient querying of connected data. However, **Jira’s own GraphQL support is very limited as of now** – Atlassian has stated that Jira is “not available to GraphQL” for third-party use yet, so developers must still use the REST API for Jira data ([What's the state of the GraphQL API for Jira - Jira Cloud - The Atlassian Developer Community](https://community.developer.atlassian.com/t/whats-the-state-of-the-graphql-api-for-jira/57093#:~:text=%40WolfgangWerner%2C))  This means no built-in facility for retrieving a subgraph in one call; you often have to make one API request for an issue, then additional requests for each linked issue, and so on.

**Workarounds for Limitations:** To mitigate these challenges, teams have taken a few approaches:
- *Use Scripting or Automation:* With apps like ScriptRunner or Jira Automation, you can write scripts that traverse links (for example, to aggregate data or flag circular links). Some scripting tools provide enhanced JQL functions (e.g., ScriptRunner adds functions to search issues by linked issue criteria, or to find issues at the end of link chains). This can partially overcome the query limitations.
- *Leverage Plugins for Visualization:* As noted earlier, several marketplace apps fill the visualization gap. For instance, **Issue Links Viewer** provides a “global graph” view that shows all links among a set of issues returned by a filter (JQL search), not just one issue’s links ([Issue Links Viewer | Atlassian Marketplace](https://marketplace.atlassian.com/apps/1216207/issue-links-viewer#:~:text=See%20all%20links%20between%20issues,from%20the%20JQL%20Search))  Others like *Structure* or *BigPicture* allow you to build structured views (trees or Gantt charts) of linked items which, while not free-form graphs, cover common use cases like dependency trees. There are also apps specifically designed to render issue link diagrams and even allow editing links through a graph UI (e.g., dragging nodes to create new links) ([Issue Links Viewer | Atlassian Marketplace](https://marketplace.atlassian.com/apps/1216207/issue-links-viewer#:~:text=Key%20highlights%20of%20the%20app,in%20a%20slick%2C%20visual%20way))  ([Issue Links Viewer | Atlassian Marketplace](https://marketplace.atlassian.com/apps/1216207/issue-links-viewer#:~:text=See%20all%20links%20between%20issues,from%20the%20JQL%20Search))  These tools greatly improve usability, essentially treating Jira as a backend and providing the missing “graph front-end.”
- *Export to a Graph Database:* For heavy analysis, a common strategy is to **sync Jira data to a dedicated graph database like Neo4j**. This can be done via scheduled scripts or integration tools. For example, one Jira user demonstrated exporting Jira issues and links into Neo4j to run complex graph queries and visualizations ([This Week: Rails Integration, ML for Graphs & More - Neo4j](https://neo4j.com/blog/this-week-in-neo4j-slack-integration-alteryx-machine-learning-deep-learning-on-graph-and-more/#:~:text=This%20Week%3A%20Rails%20Integration%2C%20ML,the%20data%20to%20Neo4j%20Aura))  Atlassian’s own example tutorial shows how to use the REST API and Google Charts to graph issue relationships externally ([JIRA REST API Version 2 Tutorial 8946379](https://developer.atlassian.com/server/jira/platform/jira-rest-api-version-2-tutorial-8946379/#:~:text=Example%20))  There’s also a Jira plugin for *jQAssistant* (a structural analysis tool) that scans Jira via the REST API and imports the issues and their links into a Neo4j database for analysis ([GitHub - softvis-research/jqa-jira-plugin: This is a Jira parser for jQAssistant. It enables jQAssistant to scan and to analyze data from Jira.](https://github.com/softvis-research/jqa-jira-plugin#:~:text=jqassistant.sh%20scan%20))  Once in a graph database, you can use Cypher queries or GraphQL to explore the network in ways Jira cannot (e.g., find cycles, shortest paths, impact analysis, etc.). The results of those analyses can then be fed back into Jira reports or Confluence pages for the team to review.

In summary, Jira’s linking system gives you the **basic graph structure**, but you will likely need add-ons or external tooling to overcome the analytical and visualization limitations. It’s wise to anticipate these needs – if your use case requires heavy graph traversal, plan to integrate Jira with a graph engine or choose an app that provides the needed functionality.

## Tools and Integrations to Enhance Graph Capabilities

Because of the above limitations, a variety of **tools, plugins, and integrations** have emerged to make Jira more graph-friendly:

- **Visualization Plugins:** The Atlassian Marketplace offers several apps to visualize issue networks. For instance, *Link Hierarchy*, *Issue Links Viewer*, *STAGIL Issue Maps & Graphs*, and *Pathfinder* are plugins that display a graph of issues with nodes and edges corresponding to issues and links ([
	Solved: Visual overview of related and blocked issues?
](https://community.atlassian.com/t5/Jira-questions/Visual-overview-of-related-and-blocked-issues/qaq-p/757970#:~:text=Although%20I%20am%20not%20particularly,and%20the%20link%20between%20those))  These typically allow interactive exploration: you might click a node to expand its linked issues, change the layout, or filter by link type. They often use color-coding for issue types or statuses, and different arrow styles for link types ([Issue Graph | Atlassian Marketplace](https://marketplace.atlassian.com/apps/1213005/issue-graph#:~:text=Visualizes%20your%20issues%27%20dependencies%20at,once))  For example, *Issue Links Viewer* lets you generate a **graph of all links in a set of issues** (from a JQL query) and even create or remove links via the graph UI ([Issue Links Viewer | Atlassian Marketplace](https://marketplace.atlassian.com/apps/1216207/issue-links-viewer#:~:text=See%20all%20links%20between%20issues,from%20the%20JQL%20Search))  ([Issue Links Viewer | Atlassian Marketplace](https://marketplace.atlassian.com/apps/1216207/issue-links-viewer#:~:text=Key%20highlights%20of%20the%20app,in%20a%20slick%2C%20visual%20way))  *STAGIL Issue Maps* provides multi-level graph views (beyond one hop) and filtering by fields or link types, essentially giving a dynamic “mind map” of Jira issues ([STAGIL Issue Maps & Graphs – Visualize issues and their links!](https://www.stagil.com/products/stagil-apps-for-jira/stagil-issue-maps#:~:text=Issue%20Maps%20%26%20Link%20Dependencies))  ([STAGIL Issue Maps & Graphs – Visualize issues and their links!](https://www.stagil.com/products/stagil-apps-for-jira/stagil-issue-maps#:~:text=Search%20by%20links%20%26%20Advanced,Links%20integration))  These tools greatly aid in **understanding and managing a graph modeled in Jira**, turning raw link data into a navigable diagram.

- **Planning and Dependency Management Tools:** There are project management extensions like *BigPicture*, *Portfolio (Advanced Roadmaps)*, and *Structure* that focus on dependencies and hierarchies. While their primary purpose is planning (e.g., Gantt charts, agile roadmaps), they indirectly enhance graph usage by providing views of issue dependencies (a subset of the graph). BigPicture/BigGantt, for example, use the “blocks” link to build a dependency timeline. Structure allows building a custom issue hierarchy which can include linked issues. These aren’t generic graph explorers, but if your graph use-case is specifically task dependency management, they are worth mentioning. They also sometimes provide roll-up calculations or warnings for dependency conflicts, which addresses some limitations of Jira’s bare links.

- **GraphQL Interfaces:** As noted, Jira’s native GraphQL API for cloud is not fully open for issue data yet ([What's the state of the GraphQL API for Jira - Jira Cloud - The Atlassian Developer Community](https://community.developer.atlassian.com/t/whats-the-state-of-the-graphql-api-for-jira/57093#:~:text=%40WolfgangWerner%2C))  However, there are third-party approaches. Some developers use GraphQL wrappers over Jira’s REST API, allowing clients to query Jira data with GraphQL. For example, one could use tools like **N8N** or custom Node.js servers to fetch linked issues recursively and expose a GraphQL endpoint for queries. Additionally, certain Jira apps or related products provide GraphQL endpoints – for instance, Xray (a test management add-on) has a GraphQL API for test entities (not Jira issues per se, but related data). There’s also an app called *GraphQL Playground+ for Jira* ([GraphQL Playground+ for Jira - Atlassian Marketplace](https://marketplace.atlassian.com/apps/1225930/graphql-playground-for-jira?tab=overview#:~:text=GraphQL%20Playground%2B%20for%20Jira%20,multiple%20tabs%20with%20notes%2C)) which suggests embedding GraphQL queries in Jira, though it appears to be more about interacting with external GraphQL from Jira (not querying Jira itself via GraphQL). In summary, **GraphQL is an emerging option** to query Jira data in a graph-friendly way, but it usually involves setting up a proxy or waiting for Atlassian to expand official support. If GraphQL becomes fully available for Jira, one could retrieve an issue and its connected issues (and their connections) in a single query, which would be very powerful for graph traversals.

- **Integration with Neo4j and Graph Databases:** For advanced use, some teams integrate Jira with graph databases. This can be as simple as periodic exports: e.g., a Python script that pulls all issues and links via REST and upserts them into a Neo4j database. From there, one might use Neo4j’s Bloom or Browser to visualize and query. There are community examples of this: one engineer wrote about using **GraphXR (a graph visualization tool) to load Jira issues and then save the graph to Neo4j Aura**, effectively merging Jira data with other sources to analyze company relationships ([This Week: Rails Integration, ML for Graphs & More - Neo4j](https://neo4j.com/blog/this-week-in-neo4j-slack-integration-alteryx-machine-learning-deep-learning-on-graph-and-more/#:~:text=This%20Week%3A%20Rails%20Integration%2C%20ML,the%20data%20to%20Neo4j%20Aura))  Another example is the *jQAssistant Jira plugin* which we mentioned – it automates pulling Jira data into Neo4j so you can run analyses and even feed results back into Jira or reports ([GitHub - softvis-research/jqa-jira-plugin: This is a Jira parser for jQAssistant. It enables jQAssistant to scan and to analyze data from Jira.](https://github.com/softvis-research/jqa-jira-plugin#:~:text=jqassistant.sh%20scan%20))  While not a one-click solution, these integrations **turn Jira into a hybrid solution**: Jira maintains the data entry and workflow, while the graph database provides deep query and analysis capabilities (e.g., running Cypher queries to find clusters of related issues or performing graph-based machine learning on your Jira data).

- **Reporting and Traceability Add-ons:** There are also apps like *Issue Traceability Matrix* ([Issue Traceability Matrix for Jira - Atlassian Marketplace](https://marketplace.atlassian.com/apps/1218414/issue-traceability-matrix-for-jira#:~:text=Issue%20Traceability%20Matrix%20for%20Jira,development%20information%20in%20Jira%20issues)) which focus on presenting the relationships in a matrix or report format (useful for compliance or coverage analysis). These aren’t graphs visually, but they are built on the same link data and help navigate the relationships (for example, listing all tests linked to each requirement). They enhance Jira’s capability to *use* the graph data in practical ways (e.g., ensuring every requirement has at least one test linked, etc.).

In choosing tools, consider your primary goals. If you need to **visualize and navigate** the graph frequently, a dedicated graph viewer add-on is invaluable. If you mostly need to **compute or analyze** things about the graph, exporting to Neo4j or using a reporting plugin might be better. Many teams use a combination: keep the day-to-day usage within Jira (with perhaps a lightweight viewer plugin for quick visuals) and do heavy analysis in external systems periodically.

## Real-World Examples

Several organizations and projects have utilized Jira in a graph-like fashion:

- **Photobox (Security Knowledge Graph):** The CISO of Photobox (an online photo company) publicly discussed using Jira to map security-related knowledge as a graph. In a DevSecCon presentation, he described that **his team treats Jira as a “Graph Database”**, with issues capturing security risks and tasks, and Jira linkages (including Epic links and regular links) representing relationships between them ([Thinking in graphs v1.0 | PPT](https://www.slideshare.net/slideshow/thinking-in-graphs-v10/101283923#:~:text=,))  They enriched this setup by using labels and custom fields as attributes on the nodes, and Epics as higher-level grouping nodes (e.g., an Epic representing a project that “captures all risks and tasks” related to it) ([Thinking in graphs v1.0 | PPT](https://www.slideshare.net/slideshow/thinking-in-graphs-v10/101283923#:~:text=,TimeStamps%20Linked%20to%20Epic))  The team then used Confluence to visualize or query this data, effectively turning the combination of Jira+Confluence into a graph management system for security. This example shows that even outside of software development, Jira can be repurposed to track complex interconnected information (in this case, security issues, controls, incidents, etc.).

- **Development Traceability at Scale:** Many software organizations use Jira links to achieve traceability between artifacts – for instance, linking a “Story” to the “Epic” it belongs to, linking a “Bug” to the “Story” it impacts, linking “Requirement” issues to “Test Case” issues (when using Jira for requirements management), and linking code-related issues (like Git commits or pull requests via dev integrations) to the stories or tasks. One case is using Jira for **Requirements Traceability Matrix** generation, where each requirement is an issue linked to one or more implementation tickets and test cases. Tools like the *Xray* test management add-on leverage issue links to build a graph of Requirement → Test → Test Execution, providing reports to ensure coverage. An Atlassian Community article notes that while Jira doesn’t enforce traceability, simply having the links recorded (“these two issues are related”) forms a basis on which you can build such traceability reports ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=First%20of%20all%2C%20what%20are,One))  Some teams also link Jira issues to Confluence pages or external systems for knowledge linking. For example, a design doc in Confluence might be linked to the Jira feature ticket it pertains to – creating a node for the document in the “graph”.

- **Dependency Mapping in Large Projects:** In big software projects or programs, it’s common to have a web of inter-project dependencies (e.g., a mobile app issue is blocked by an API issue in a different project). Jira’s linking is heavily used here. Organizations like large banks or tech enterprises have thousands of issues with “blocks” links representing an intricate dependency graph. They often use tools like Structure, BigPicture, or custom dashboards to monitor these. While specific company names are seldom published for this, Atlassian’s own JIRA instance (for their cloud development) is known to have many interlinked issues for feature tracking. The demand for a **“link map” feature in Jira**  ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=A%20,in%20a%20given%20project)) originally came from users in such scenarios who wanted to see all related issues in one view. Although Atlassian didn’t implement it directly, these use-cases are now served by third-party apps. For example, game development companies (with complex task webs: assets, code tasks, testing tasks all interdependent) have reported success using a graph view plugin to manage issue dependencies visually instead of combing through lists.

- **Kineviz (GraphXR) Example:** Kineviz, a company focused on graph visualization, demonstrated using their tool *GraphXR* to integrate with Jira. An engineer, Ben Goosman, wrote about **visualizing Jira issues in GraphXR** and then exporting that data to Neo4j for further analysis ([This Week: GraphQL, GraphXR, Marvel Studios API & More - Neo4j](https://neo4j.com/blog/this-week-in-neo4j-graphql-graphxr-marvel-studios-api-speech-to-cypher-free-training-and-more/#:~:text=In%20this%20blog%2C%20Ben%20Goosman,managed%20in%20Jira%2C%20Airtable%2C))  ([This Week: Rails Integration, ML for Graphs & More - Neo4j](https://neo4j.com/blog/this-week-in-neo4j-slack-integration-alteryx-machine-learning-deep-learning-on-graph-and-more/#:~:text=This%20Week%3A%20Rails%20Integration%2C%20ML,the%20data%20to%20Neo4j%20Aura))  In his case, the graph combined Jira data with data from Airtable to see a broader picture of company workflows. This example is noteworthy because it shows a small company treating Jira as one of multiple data sources in a larger knowledge graph, highlighting that Jira’s issue-link data is accessible enough to plug into graph analytics pipelines.

Each of these examples underlines a common theme: **Jira’s flexibility allows creative uses to manage graph-structured data**, but success often hinges on using the right extensions or complementary tools. Whether it’s for security knowledge, requirements traceability, project dependency management, or blending with other databases, many have proven it’s possible to get value out of Jira-as-a-graph.

## Alternatives and Considerations

While Jira can be cajoled into acting like a graph database, it’s important to consider alternatives or complementary solutions, especially if your use-case is very graph-intensive:

- **Dedicated Graph Databases:** If you truly need to perform complex graph queries (shortest paths, graph ML, subgraph isomorphism, etc.) or handle highly connected data at scale, a graph database like Neo4j, Amazon Neptune, or an RDF store might be more appropriate. These systems are built to store nodes and edges efficiently and provide powerful query languages (Cypher, SPARQL) for traversing relationships. One approach is to use Jira for what it’s best at (workflow, tracking, UI) but offload the graph crunching to a graph DB. You can **sync Jira issues to a graph database** (as discussed earlier) on a schedule. The graph DB becomes the source for complex analysis and perhaps even an alternate visualization (for example, using Neo4j Bloom to allow non-technical users to explore the network with a nice interface). The downside is maintaining the sync and dealing with data in two places, but for heavy graph needs this separation of concerns can be worth it. Essentially, **Jira would act as the entry point and record system, and the graph DB as the analytical engine**.

- **Requirements Management or ALM Tools:** Jira is a general tracker, but there are specialized tools (often used in enterprise or systems engineering) that natively support item relationships and graphs. For instance, tools like IBM Rational DOORS, Jama Connect, or others often provide visual traceability matrices and dependency graphs for requirements, tests, and tasks. If your primary goal is to handle, say, complex requirement-to-system-component mapping with versioning, a purpose-built requirements management tool might be easier in the long run, with Jira perhaps integrated for execution tracking. In the Atlassian ecosystem, some rely on **Confluence** for building manual diagrams or using draw.io to map out relationships, but those lack the dynamic update you get from Jira links. The user who suggested a Jira link graph noted that such a feature would put Jira in competition with dedicated requirements engineering tools where dependency maps are standard ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=I%20believe%20that%20once%20you,more%20ideas%20will%20come%20up))  This hints that outside Jira, those tools might serve the need if an organization is willing to adopt them (though they come with their own complexity and cost).

- **Graph-Powered Apps:** Another alternative is to use an app that is inherently graph-based to manage your data, and integrate it with Jira. For example, some have used Trello or Airtable for certain relationships and linked them to Jira (though Trello is not graph-oriented beyond simple card links). There are newer SaaS platforms (notably in the enterprise architecture or knowledge management space) that use graph databases under the hood to allow flexible linking of data (for instance, tools like **Compass** by Atlassian is a newer product for tracking software architecture components in a graph-like way, though still evolving). If your use-case aligns with one of those tools (like modeling a network of services, or a knowledge graph of documentation), it might be worth evaluating them rather than bending Jira to fit. That said, many of these can integrate back to Jira (e.g., Compass can link to Jira tickets) to keep the development workflow connected.

- **Do Nothing (Keep It Simple):** It’s worth questioning the necessity of storing certain data as issues in Jira. If the “graph” you have in mind is very data-centric and not issue-centric (for example, modeling relationships between static entities like products, customers, servers, etc.), sometimes a better approach is a CMDB (Configuration Management Database) or a simple spreadsheet, rather than Jira. Jira issues come with overhead (workflow, assignees, etc.) which might not be needed for pure data storage. In such cases, an alternative is to use Jira only when that data becomes actionable (like create an issue when there’s a task or incident) and manage the reference data in a more suitable repository. For instance, if you considered using Jira issues to model all employees and their org chart (a graph of reporting relationships), a dedicated HR system or even a graph DB would be more natural, and you’d only create Jira issues when there’s an action related to an employee. Always weigh whether using Jira in this way will simplify your life or if it’s adding a layer of indirection.

**Summary of Alternatives:** If Jira’s graph capabilities fall short, you can either **extend Jira** (with plugins, integrations) or **pair Jira with other systems**. Dedicated graph solutions will outshine Jira in querying and visualizing networks, but Jira excels in integrating those networks with project activity. Many organizations find a hybrid approach works – Jira for day-to-day and a graph database or reporting tool for strategic analysis. The right path depends on your specific needs, team skills, and tool budget. It’s not uncommon to start modeling in Jira as a quick solution and then, as the data/complexity grows, transition to a more purpose-built system once the concept is proven.

## Conclusion

Jira’s issue linking system provides a *surprisingly powerful foundation* for representing graph-like data. By treating issues as nodes and links as edges, teams have modeled everything from task dependency networks to knowledge graphs within Jira. The benefits of this approach lie in leveraging Jira’s familiar interface, traceability features, and integration ecosystem – effectively getting a “graph database lite” embedded in your project management tool. However, Jira is not optimized as a graph database, and users will encounter limitations in querying, visualization, and scale as their graphs grow in complexity. Best practices such as clearly defining link types, structuring issue types for nodes, and keeping the graph curated become important to make this workable.

To get the most out of Jira as a graph, one typically needs to augment it with additional tools: marketplace apps can render interactive graphs of issues ([
	Solved: Visual overview of related and blocked issues?
](https://community.atlassian.com/t5/Jira-questions/Visual-overview-of-related-and-blocked-issues/qaq-p/757970#:~:text=Although%20I%20am%20not%20particularly,and%20the%20link%20between%20those))  and external systems like Neo4j can take over when deep graph analytics are required ([This Week: Rails Integration, ML for Graphs & More - Neo4j](https://neo4j.com/blog/this-week-in-neo4j-slack-integration-alteryx-machine-learning-deep-learning-on-graph-and-more/#:~:text=This%20Week%3A%20Rails%20Integration%2C%20ML,the%20data%20to%20Neo4j%20Aura))  Real-world usage shows that with creativity, Jira can track complex relationships (the Photobox security example being a prime case of Jira as an internal knowledge graph ([Thinking in graphs v1.0 | PPT](https://www.slideshare.net/slideshow/thinking-in-graphs-v10/101283923#:~:text=,)) , but also that one must be mindful of Jira’s constraints. 

In summary, Jira can **support graph-like relationships** through its flexible linking, and it’s a viable solution for many scenarios where a full graph database might be overkill. It works best when the graph ties closely to actionable work items or when team members are already working in Jira. For more intensive graph needs, consider a hybrid approach or alternate tools, using Jira as one piece of a larger puzzle. By understanding these implementation details, benefits, and challenges, you can make an informed decision on modeling your graph data in Jira and choose the right extensions to fill any gaps, thereby creating a robust solution that combines Jira’s strengths with the power of graph data representation.

**References:**

- Atlassian Community – *“Visual overview of related and blocked issues?”* (Jira issue links visualized as a graph) ([
	Solved: Visual overview of related and blocked issues?
](https://community.atlassian.com/t5/Jira-questions/Visual-overview-of-related-and-blocked-issues/qaq-p/757970#:~:text=Although%20I%20am%20not%20particularly,and%20the%20link%20between%20those))  
- Atlassian Marketplace – *Issue Graph* plugin description (issues as nodes, links as edges) ([Issue Graph | Atlassian Marketplace](https://marketplace.atlassian.com/apps/1213005/issue-graph#:~:text=Visualizes%20your%20issues%27%20dependencies%20at,once))  
- Atlassian Community – User suggestion for a link dependency map (need for whole-picture graph of issue links) ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=When%20viewing%20an%20issue%20you,node%20%28or%20link%29%20away))  ([Loading...](https://jira.atlassian.com/browse/JRASERVER-2544#:~:text=A%20,in%20a%20given%20project))  
- Atlassian Developer Tutorial – *“Graphing issue links”* example (using REST API to graph relationships between issues) ([JIRA REST API Version 2 Tutorial 8946379](https://developer.atlassian.com/server/jira/platform/jira-rest-api-version-2-tutorial-8946379/#:~:text=Example%20))  
- *Jira Issue Links and Dependencies Management* (Atlassian Community article on using links for relationships and dependencies) ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=First%20of%20all%2C%20what%20are,showing%20dependencies%20between%20different%20issues))  ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=Does%20Outward%20or%20Inward%20Description,more%20on%20this%20later))  ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=%5BImage%203%3A%20Jira))  
- Stiltsoft Blog – *Organizing a Jira Issue* (on linking issues and customizing link types for flexibility) ([Best Practices for Organizing a Jira Issue - Stiltsoft](https://stiltsoft.com/blog/best-practices-for-organizing-a-jira-issue/#:~:text=Issue%20linking%20allows%20you%20to,For%20example))  
- Atlassian Developer Community – *State of GraphQL API for Jira* (Jira not fully available via GraphQL as of 2022) ([What's the state of the GraphQL API for Jira - Jira Cloud - The Atlassian Developer Community](https://community.developer.atlassian.com/t/whats-the-state-of-the-graphql-api-for-jira/57093#:~:text=%40WolfgangWerner%2C))  
- Atlassian Community – *“Getting Jira Issue field Values via GraphQL”* (user attempting multi-level data via GraphQL) ([
	Solved: Getting Jira Issue field Values via GraphQL
](https://community.atlassian.com/t5/Jira-questions/Getting-Jira-Issue-field-Values-via-GraphQL/qaq-p/2509541#:~:text=I%20am%20trying%20to%20do,contents%20of%20the%20Security%20tab)) (GraphQL in Jira context)  
- Atlassian Community – Q&A on issue linking (links are just markers of relationship, no built-in logic) ([
	Jira Issue Links and dependencies management - Atlassian Community
](https://community.atlassian.com/t5/App-Central-articles/Jira-Issue-Links-and-dependencies-management/ba-p/2050756#:~:text=First%20of%20all%2C%20what%20are,One))  
- Atlassian Marketplace – *Issue Links Viewer* (global graph of all links among filtered issues) ([Issue Links Viewer | Atlassian Marketplace](https://marketplace.atlassian.com/apps/1216207/issue-links-viewer#:~:text=See%20all%20links%20between%20issues,from%20the%20JQL%20Search))  
- STAGIL Issue Maps & Graphs – product page (multi-level graph visualization, search by links) ([STAGIL Issue Maps & Graphs – Visualize issues and their links!](https://www.stagil.com/products/stagil-apps-for-jira/stagil-issue-maps#:~:text=Issue%20Maps%20%26%20Link%20Dependencies))  ([STAGIL Issue Maps & Graphs – Visualize issues and their links!](https://www.stagil.com/products/stagil-apps-for-jira/stagil-issue-maps#:~:text=Search%20by%20links%20%26%20Advanced,Links%20integration))  
- Atlassian Community – *“task-relation graph based on JIRA”* (tools for visualizing issue links) ([
	Solved: Visual overview of related and blocked issues?
](https://community.atlassian.com/t5/Jira-questions/Visual-overview-of-related-and-blocked-issues/qaq-p/757970#:~:text=Although%20I%20am%20not%20particularly,and%20the%20link%20between%20those))  
- SlideShare – *“Thinking in Graphs”* by Dinis Cruz (Photobox CISO) – using Jira as a graph DB with issues as nodes (security context) ([Thinking in graphs v1.0 | PPT](https://www.slideshare.net/slideshow/thinking-in-graphs-v10/101283923#:~:text=,))  
- Neo4j Community Blog – *This Week in Neo4j* (using GraphXR with Jira and Neo4j for visualization) ([This Week: Rails Integration, ML for Graphs & More - Neo4j](https://neo4j.com/blog/this-week-in-neo4j-slack-integration-alteryx-machine-learning-deep-learning-on-graph-and-more/#:~:text=This%20Week%3A%20Rails%20Integration%2C%20ML,the%20data%20to%20Neo4j%20Aura))  
- jQAssistant Jira Plugin (GitHub) – documentation on scanning Jira projects into Neo4j