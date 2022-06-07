from scripts.CDHIT_parser import get_clusters
from glob import glob
from itertools import product


# vai buscar aos .tsv criados antes, e não fica dependente dos fasta que vão ser criados
files = {threshold: glob(f"workflow/Data/Tables/cdhit_clusters_{threshold}_afterUPIMAPI.tsv") for threshold in config["thresholds"]}
threshold2clusters = {}
for thresh, path in files.items():
	threshold2clusters[thresh] = get_clusters(path[0])

# fazer uma lista de listas com todos os clusters, por ordem de threshold
big_list_clusters = [v for k, v in threshold2clusters.items()]
max_clusters = max([max(x) for x in big_list_clusters])
all_clusters = [str(i) for i in range(0, max_clusters+1)]

# função vai fazer todas as combinações entre thresholds e clusters correspondentes
def util(lista_thresholds, lista_de_listas_clusters):
	autorized_combs = []
	for threshold in range(len(lista_thresholds)):
		for cluster in lista_de_listas_clusters[threshold]:
			combinacao = (lista_thresholds[threshold], str(cluster))
			autorized_combs.append(combinacao)
	autorized_combs_frozen = {frozenset(t) for t in autorized_combs}
	return autorized_combs_frozen

# função que vai fazer o produto entre todos, e so devolve os desejados
def match_threshold_W_cluster(combinador, desired_combs) -> tuple:
    def match_threshold_W_cluster(*args, **kwargs):
        for combo in combinador(*args, **kwargs):
            if frozenset(combo) in desired_combs:
                yield combo
    return match_threshold_W_cluster

desired = util(config["thresholds"], big_list_clusters)
# inicializar função de combinação
filtered_product = match_threshold_W_cluster(product, desired)