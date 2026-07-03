import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):

        self._model.build_graph()

        self._view._txt_result.controls.clear()

        if self._model.grafo.number_of_nodes() == 0:
            self._view._txt_result.controls.append(ft.Text("Nessun grafo creato con questi parametri."))
            self._view.update_page()
            return

        nodi, archi = self._model.get_dettagli_grafo()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con successo!", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Numero Nodi: {nodi}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero Archi: {archi}"))

        # 5. RIEMPIMENTO DELLA TENDINA NODI (TRUCCO LAMBDA E KEY)
        self._view._ddAlbum.options.clear()
        nodi_ordinati = list(self._model.grafo.nodes())
        nodi_ordinati.sort(key=lambda x: x.Title)

        for nodo in nodi_ordinati:
            self._view._ddAlbum.options.append(
                ft.dropdown.Option(
                    key=str(nodo.AlbumId),
                    text=nodo.Title
                )
            )

        self._view.update_page()


    def handleStampaInfo(self,e):
        # b) Numero componenti connesse e componente maggiore
        num_comp, comp_maggiore = self._model.get_componente_connessa_maggiore()
        self._view._txt_result.controls.append(ft.Text(f"Numero di componenti connesse:  {num_comp}"))
        self._view._txt_result.controls.append(ft.Text(f"La componente connessa più grande ha {len(comp_maggiore)} album"))
        self._view._txt_result.controls.append(ft.Text(f"Dettagli degli album appartenneti alla componente connessa più grande"))
        comp_maggiore.sort(key=lambda x : x.Title)


        for nodo in comp_maggiore:
            self._view._txt_result.controls.append(ft.Text(f"{nodo.Title}: {len(nodo.tracks)} brani"))
        self._view.update_page()


    def handleSelezione(self,e):
        # ==========================================
        # 1. LETTURA E VALIDAZIONE INPUT
        # ==========================================
        # A. Recupero il nodo di partenza (es. dal menu a tendina)
        nodo_selezionato = self._view._ddAlbum.value
        if nodo_selezionato is None:
            self._view.create_alert("Attenzione: Seleziona prima un album dal menu a tendina!")
            return

        id_album = int(nodo_selezionato)
        nodo = self._model.mappa_nodi[id_album]

        # B. Recupero e valido la lunghezza inserita dall'utente
        valore_input = self._view._txtInN.value
        if not valore_input:
            self._view.create_alert("Attenzione: Inserisci un numero di album valido!")
            return

        try:
            lunghezza_input = int(valore_input)
            # Un cammino deve avere almeno un punto A e un punto B (lunghezza 2)
            if lunghezza_input < 2:
                self._view.create_alert("La lunghezza deve essere di almeno 2 nodi!")
                return
        except ValueError:
            self._view.create_alert("Attenzione: La lunghezza deve essere un numero intero valido!")
            return

        # ==========================================
        # 2. CHIAMATA AL MODEL E PULIZIA VIEW
        # ==========================================
        self._view._txt_result.controls.clear()

        # Chiamo la ricorsione passandogli il nodo (convertito se serve) e la lunghezza
        percorso_ottimo, peso_max = self._model.calcola_sottoinsieme_ottimo(lunghezza_input, nodo)

        # Controllo se ha trovato qualcosa
        if not percorso_ottimo:
            self._view._txt_result.controls.append(
                ft.Text(f"Nessun percorso di lunghezza {lunghezza_input} trovato", color="red")
            )
            self._view.update_page()
            return

        # ==========================================
        # 3. STAMPE DEI RISULTATI (Scegli quella richiesta dalla traccia)
        # ==========================================
        # Stampa dell'intestazione (Sempre utile)

        self._view._txt_result.controls.append(ft.Text(f"Trovato percorso ottimo!", color="green", weight="bold"))
        self._view._txt_result.controls.append(ft.Text(f"Numero totale album: {len(percorso_ottimo)}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero complessivo brani: {peso_max}"))

        self._view._txt_result.controls.append(ft.Text("Album selezionati:", weight="bold"))

        # Ordino per titolo come chiede la traccia
        percorso_ottimo.sort(key=lambda x: x.Title)

        for album in percorso_ottimo:
            # Ricordati di adattare 'album.GenreId' con il vero nome dell'attributo se è diverso!
            # (A volte il genere si trova dentro la lista delle tracks: album.tracks[0].GenreId)
            testo = f"-> {album.Title} (Brani: {len(album.tracks)})"
            self._view._txt_result.controls.append(ft.Text(testo))

        self._view.update_page()