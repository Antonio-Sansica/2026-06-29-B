import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.mappa_nodi = {}
        self.grafo = nx.Graph()

    def popola_mappa(self):
        self.mappa_nodi.clear()
        lista_nodi = DAO.getAllNodi()
        for nodo in lista_nodi:
            self.mappa_nodi[nodo.AlbumId] = nodo

        lista_tracks = DAO.getAllTracks()
        for track in lista_tracks:
            if track.AlbumId in self.mappa_nodi:
                album_corrispondente = self.mappa_nodi[track.AlbumId]
                album_corrispondente.tracks.append(track)


    def build_graph(self):
        self.grafo.clear()
        self.popola_mappa()

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
        # 1. Quante sono in totale?
        num_componenti = nx.number_connected_components(self.grafo)

        # 2. Ottengo una lista di "set" (insiemi) contenenti i nodi di ciascuna componente connessa
        componenti = list(nx.connected_components(self.grafo))

        # 3. Trovo quella più grande usando len() come chiave per la ricerca del massimo
        if not componenti:
            return 0, []
        comp_maggiore = max(componenti, key=len)

        return num_componenti, list(comp_maggiore)

    # =========================================================================
    # RICORSIONE 3: SOTTOINSIEMI / COMBINAZIONI (La "Scelta di K elementi")
    # === QUANDO USARLA ===
    # Quando la traccia dice: "Trova un SET di K nodi che massimizza/minimizza
    # un certo valore, rispettando dei vincoli" (Es. "nessuno dei K nodi deve
    # essere collegato agli altri").
    # === ATTENZIONE ===
    # Qui NON si usano gli archi (neighbors) per muoversi! Si pesca da una lista.
    # =========================================================================
    def calcola_sottoinsieme_ottimo(self, K, nodo_partenza):
        self._soluzione_ottima = []
        self._punteggio_ottimo = 0  # Cerchiamo il massimo, partiamo da 0

        # --- OTTIMIZZAZIONE 1: PRE-CALCOLO LE FAMIGLIE ---
        # Creo un dizionario: Chiave = Nodo, Valore = ID della componente connessa (0, 1, 2...)
        self.mappa_famiglie = {}
        componenti = list(nx.connected_components(self.grafo))

        # Se K è maggiore del numero totale di componenti, è matematicamente impossibile!
        if K > len(componenti):
            return [], 0

        for id_famiglia, comp in enumerate(componenti):
            for n in comp:
                self.mappa_famiglie[n] = id_famiglia

        # --- OTTIMIZZAZIONE 2: FILTRO IL CESTO ---
        # Trovo la famiglia del nodo di partenza
        famiglia_partenza = self.mappa_famiglie[nodo_partenza]

        # Nodi validi: Prendo tutti i nodi, ma SCARTO SUBITO quelli che sono nella stessa
        # componente connessa del nodo di partenza (perché violerebbero il vincolo dal primo step!)
        nodi_validi = [n for n in self.grafo.nodes() if self.mappa_famiglie[n] != famiglia_partenza]

        parziale = [nodo_partenza]
        self._ricorsione_sottoinsieme(parziale, nodi_validi, K, 0)

        return self._soluzione_ottima, self._punteggio_ottimo

    def _ricorsione_sottoinsieme(self, parziale, nodi_validi, K, pos):
        # 1. CONDIZIONE DI TERMINAZIONE (Ho pescato esattamente K elementi)
        if len(parziale) == K:
            # Calcolo il punteggio di questa squadra/set
            punteggio = self._calcola_punteggio_set(parziale)

            # Controllo se è il nuovo record (Usa < per MINIMO, > per MASSIMO)
            if punteggio > self._punteggio_ottimo:
                self._punteggio_ottimo = punteggio
                self._soluzione_ottima = copy.deepcopy(parziale)
            return

        # 2. TRUCCO "PRUNING" (Taglio dei rami morti) - FONDAMENTALE!
        # Se nel 'cesto' sono rimasti meno elementi di quanti me ne servono per arrivare a K,
        # è inutile continuare a cercare. Interrompo subito per non far crashare/freezare il PC.
        nodi_rimanenti_nel_cesto = len(nodi_validi) - pos
        if len(parziale) + nodi_rimanenti_nel_cesto < K:
            return

        # 3. ESPLORAZIONE
        # Parto da 'pos' (e non da 0) per NON generare permutazioni doppie (Es: A-B e B-A)
        for i in range(pos, len(nodi_validi)):
            nodo = nodi_validi[i]

            # Controllo se questo nodo può entrare in squadra
            if self._vincolo_sottoinsieme(nodo, parziale):
                parziale.append(nodo)

                # VADO IN PROFONDITÀ.
                # 🚨 PASSO i + 1: Questo mi vieta di ripescare lo stesso nodo!
                self._ricorsione_sottoinsieme(parziale, nodi_validi, K, i + 1)

                # BACKTRACKING
                parziale.pop()

    def _calcola_punteggio_set(self, parziale):
        # --- SOSTITUISCI CON LA MATEMATICA DELLA TRACCIA ---
        # Es. Se cerco la differenza tra il più giovane e il più vecchio:
        punteggio = 0
        for album in parziale:
            punteggio += len(album.tracks)

        return punteggio

    def _vincolo_sottoinsieme(self, nodo_candidato, parziale):
        # Recupero istantaneamente l'ID dal dizionario pre-calcolato
        famiglia_candidato = self.mappa_famiglie[nodo_candidato]

        # Controllo se qualcuno in 'parziale' ha la stessa targhetta
        for nodo_in_squadra in parziale:
            famiglia_in_squadra = self.mappa_famiglie[nodo_in_squadra]
            if famiglia_candidato == famiglia_in_squadra:
                return False

        return True




