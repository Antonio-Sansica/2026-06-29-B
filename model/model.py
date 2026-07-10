import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.mappa_nodi = {}
        self.lista_tracce = []
        self.grafo = nx.Graph()
        self.popola_mappa_nodi()

    def popola_mappa_nodi(self):
        self.mappa_nodi.clear()
        lista_nodi = DAO.getAllNodi()
        lista_tracce = DAO.getAllTracks()
        for nodo in lista_nodi:
            self.mappa_nodi[nodo.AlbumId] = nodo
            for track, album in lista_tracce:
                if album == nodo.AlbumId:
                    self.mappa_nodi[nodo.AlbumId].tracks.append(track)

    def build_graph(self):
        self.grafo.clear()

        self.grafo.add_nodes_from(self.mappa_nodi.values())

        archi_grezzi = DAO.getAllArchi()

        for id_1, id_2 in archi_grezzi:
            if id_1 in self.mappa_nodi and id_2 in self.mappa_nodi:
                n1 = self.mappa_nodi[id_1]
                n2 = self.mappa_nodi[id_2]
                self.grafo.add_edge(n1, n2)

    def get_dettagli_grafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def get_numero_componenti_connesse(self):
        if self.grafo.number_of_nodes() == 0: return 0
        return nx.number_connected_components(self.grafo)

    def get_componente_connessa_maggiore(self):
        num_componenti = nx.number_connected_components(self.grafo)

        componenti = list(nx.connected_components(self.grafo))

        if not componenti:
            return []
        comp_maggiore = max(componenti, key=len)

        return list(comp_maggiore)




    def calcola_sottoinsieme_ottimo(self, K, nodo_partenza):
        self._soluzione_ottima = []
        self._punteggio_ottimo = 0

        # --- OTTIMIZZAZIONE 1: PRE-CALCOLO LE FAMIGLIE (Componenti Connesse) ---
        self.mappa_famiglie = {}
        componenti = list(nx.connected_components(self.grafo))

        # Se K è maggiore del numero totale di componenti, è matematicamente impossibile!
        if K > len(componenti):
            return [], 0

        for id_famiglia, comp in enumerate(componenti):
            for n in comp:
                self.mappa_famiglie[n] = id_famiglia

        famiglia_partenza = self.mappa_famiglie.get(nodo_partenza, None)

        # Nodi validi: Prendo tutti i nodi, ma SCARTO SUBITO quelli che sono nella stessa
        # componente connessa del nodo di partenza (perché violerebbero il vincolo dal primo step!)
        nodi_validi = [n for n in self.grafo.nodes() if self.mappa_famiglie[n] != famiglia_partenza]

        # Il nodo di partenza entra di diritto nella squadra
        parziale = [nodo_partenza]

        # Faccio partire la ricorsione da posizione 0
        self._ricorsione_sottoinsieme(parziale, nodi_validi, K, 0)

        return self._soluzione_ottima, self._punteggio_ottimo

    def _ricorsione_sottoinsieme(self, parziale, nodi_validi, K, pos):
        # 1. CONDIZIONE DI TERMINAZIONE (Ho pescato esattamente K elementi)
        if len(parziale) == K:
            # Calcolo il punteggio di questa squadra/set
            punteggio = self._calcola_punteggio_set(parziale)

            # Controllo se è il nuovo record MAX
            if punteggio > self._punteggio_ottimo:
                self._punteggio_ottimo = punteggio
                # Uso list() invece di deepcopy() per non rallentare l'algoritmo
                self._soluzione_ottima = list(parziale)
            return

        # 2. PRUNING (Taglio dei rami morti)
        nodi_rimanenti_nel_cesto = len(nodi_validi) - pos
        if len(parziale) + nodi_rimanenti_nel_cesto < K:
            return

        # 3. ESPLORAZIONE
        for i in range(pos, len(nodi_validi)):
            nodo_candidato = nodi_validi[i]

            # Controllo se questo nodo può entrare in squadra
            if self._vincolo_sottoinsieme(nodo_candidato, parziale):
                parziale.append(nodo_candidato)

                # VADO IN PROFONDITÀ (i + 1 per non ripescare lo stesso nodo)
                self._ricorsione_sottoinsieme(parziale, nodi_validi, K, i + 1)

                # BACKTRACKING
                parziale.pop()

    def _calcola_punteggio_set(self, parziale):
        punteggio = 0
        for nodo in parziale:
            # Sostituisci '.tracks' con la lista o l'attributo reale da sommare all'esame!
            punteggio += len(nodo.tracks)
        return punteggio

    def _vincolo_sottoinsieme(self, nodo_candidato, parziale):
        # Recupero istantaneamente l'ID dal dizionario pre-calcolato
        famiglia_candidato = self.mappa_famiglie[nodo_candidato]

        # Controllo se qualcuno in 'parziale' ha la stessa targhetta
        for nodo_in_squadra in parziale:
            famiglia_in_squadra = self.mappa_famiglie.get(nodo_in_squadra, None)
            if famiglia_candidato == famiglia_in_squadra:
                return False

        return True



