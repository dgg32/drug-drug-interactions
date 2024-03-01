

# Introduction
  

This repository contains code and data for my article "[Know Your Drugs: A Knowledge Graph for Drug-Drug-Disease Interactions](https://dgg32.medium.com/know-your-drugs-a-knowledge-graph-for-drug-drug-disease-interactions-a0629d192419)". 



# Prerequisite

Neo4j Desktop or AuraDB

UMLS account

Optional: a local Milvus installation
  

# Run
1. Set up the databases as described in the article. 
  

2. Fill the necessary API key information in config.yaml

3. Run 
```
preprocess.ipynb
```

and then run

```
pubchem.ipynb
```

to convert the drug to nodes and edges

4. Import the data into Neo4j


## Authors

  

*  **Sixing Huang** - *Concept and Coding*

  

## License

  

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
