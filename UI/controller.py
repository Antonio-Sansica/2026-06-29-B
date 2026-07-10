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
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con successo!"))
        self._view._txt_result.controls.append(ft.Text(f"Numero Nodi: {nodi}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero Archi: {archi}"))

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
        self._view._txt_result.controls.clear()
        num_comp = self._model.get_numero_componenti_connesse()
        comp_maggiore = self._model.get_componente_connessa_maggiore()
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {num_comp} componenti connesse"))
        self._view._txt_result.controls.append(ft.Text(f"Componente più grande ({len(comp_maggiore)} album):"))
        comp_maggiore.sort(key=lambda x : x.Title)

        for nodo in comp_maggiore:
            self._view._txt_result.controls.append(ft.Text(f"{nodo.Title}: {len(nodo.tracks)} brani"))
        self._view.update_page()

    def handleSelezione(self,e):
        # 1. Prendo il VALORE STRINGA dal Dropdown (es. l'ID dell'album)
        valore_selezionato = self._view._ddAlbum.value
        if valore_selezionato is None:
            self._view.create_alert("Attenzione: Seleziona prima un album dal menu a tendina!")
            return

        # 2. CERCO L'OGGETTO VERO E PROPRIO NELLA MAPPA NODI DEL MODELLO
        # (Assicurati di usare il casting corretto se le chiavi della tua mappa_nodi sono interi!)
        try:
            # Se la tua mappa_nodi usa interi come chiavi:
            nodo_selezionato = self._model.mappa_nodi[int(valore_selezionato)]

            # Se la tua mappa_nodi usa stringhe come chiavi, usa:
            # nodo_selezionato = self._model.mappa_nodi[valore_selezionato]
        except KeyError:
            self._view.create_alert("Errore: Impossibile trovare l'album selezionato.")
            return


        valore_input = self._view._txtInN.value
        if not valore_input:
            self._view.create_alert("Attenzione: Inserisci una lunghezza per il percorso!")
            return

        try:
            lunghezza_input = int(valore_input)
            if lunghezza_input < 2:
                self._view.create_alert("La lunghezza deve essere di almeno 2 nodi!")
                return
        except ValueError:
            self._view.create_alert("Attenzione: La lunghezza deve essere un numero intero valido!")
            return

        self._view._txt_result.controls.clear()

        percorso_ottimo, punteggio_ottimo = self._model.calcola_sottoinsieme_ottimo(lunghezza_input, nodo_selezionato)

        if not percorso_ottimo:
            self._view._txt_result.controls.append(
                ft.Text(f"Nessun percorso di lunghezza {lunghezza_input} trovato.")
            )
            self._view.update_page()
            return

        self._view._txt_result.controls.append(
            ft.Text(f"Trovato percorso ottimo! Numero album: {len(percorso_ottimo)}, Numero brani totali: {punteggio_ottimo}"))

        self._view._txt_result.controls.append(ft.Text("Nodi attraversati:"))

        percorso_ottimo.sort(key=lambda x : x.Title)
        for nodo in percorso_ottimo:
            self._view._txt_result.controls.append(ft.Text(f"-> {nodo}"))
        self._view.update_page()