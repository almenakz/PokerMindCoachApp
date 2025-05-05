# -*- coding: utf-8 -*-
# --- Imports ---
import sys
import os
import time
import random
from kivy.app import App # Restored
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.metrics import dp # Restored
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty, ObjectProperty, ListProperty

# --- Font Registration (SIMPLIFIED) ---
from kivy.core.text import LabelBase

FONT_FILENAME = 'DejaVuSans.ttf' # User must place this file next to the script!
CUSTOM_FONT_NAME = 'CardSymbolsFont'

try:
    # Simplest attempt: register by filename. Kivy should search common paths, including the script's directory.
    LabelBase.register(name=CUSTOM_FONT_NAME, fn_regular=FONT_FILENAME)
    print(f"INFO: Tentative d'enregistrement de '{FONT_FILENAME}' sous le nom '{CUSTOM_FONT_NAME}'.")
except Exception as e:
    # Catch any error during registration
    print(f"ATTENTION: Erreur lors de l'enregistrement de la police '{FONT_FILENAME}'.")
    print(f"Assurez-vous que le fichier est présent à côté du script.")
    print(f"Erreur détaillée: {e}")
    print(f"ATTENTION: Les symboles des cartes risquent de ne pas s'afficher.")
# --- END FONT REGISTRATION ---
# ---------------------------------

# --- App Class ---
class PokerMindCoachApp(App):
    # ... (rest of the code IDENTICAL to the previous version) ...
    # Including __init__, build (with font_name=CUSTOM_FONT_NAME on Spinners), on_stop,
    # update_label_text_size, on_card_select, create_option_row, on_toggle_select,
    # start_analysis_visuals, update_progress, analyser, analyser_logique, update_rect
    # Ensure analyser_logique uses the version with corrected break/elif syntax.

    # --- Properties and Init (Keep same) ---
    hand_card1 = StringProperty('?')
    hand_card2 = StringProperty('?')
    flop_card1 = StringProperty('?')
    flop_card2 = StringProperty('?')
    flop_card3 = StringProperty('?')
    log_file_handle = None
    CARDS_ID_TO_NAME = {}
    CARD_IDS = []
    CARD_NAMES = ['?']
    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ranks = ['A', 'K', 'Q', 'J', '0', '9', '8', '7', '6', '5', '4', '3', '2']; suits = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}; rank_names = {'A': 'As', 'K': 'Roi', 'Q': 'Dame', 'J': 'Valet', '0': '10'}
        for rank in ranks:
            for suit_id, suit_symbol in suits.items():
                card_id = f'{rank}{suit_id}'; rank_name = rank_names.get(rank, rank); card_name = f"{rank_name} {suit_symbol}"
                self.CARD_IDS.append(card_id); self.CARD_NAMES.append(card_name); self.CARDS_ID_TO_NAME[card_id] = card_name

    # --- Build Method (Keep previous Spinner version, ensure Spinners use font_name=CUSTOM_FONT_NAME) ---
    def build(self):
        # --- File Logging (Keep same) ---
        log_file_path = ""; original_stdout = sys.stdout; original_stderr = sys.stderr
        print(f"DEBUG: self.user_data_dir = {self.user_data_dir}", file=original_stdout)
        download_dir = '/storage/emulated/0/Download'; log_file_path = os.path.join(download_dir, 'pokermindcoach_LOG.txt')
        print(f"DEBUG: Essai de chemin log: {log_file_path}", file=original_stdout)
        try:
            if not os.path.exists(download_dir): print(f"ATTENTION: Dossier Download '{download_dir}' non trouvé.", file=original_stderr)
            print(f"INFO: Tentative d'ouverture de {log_file_path} en écriture...", file=original_stdout)
            PokerMindCoachApp.log_file_handle = open(log_file_path, 'w', encoding='utf-8')
            sys.stdout = PokerMindCoachApp.log_file_handle; sys.stderr = PokerMindCoachApp.log_file_handle
            print(f"--- Log démarré ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---"); print(f"Chemin du fichier log utilisé: {log_file_path}")
        except Exception as e:
            sys.stdout = original_stdout; sys.stderr = original_stderr; print(f"ERREUR CRITIQUE: Impossible de rediriger la sortie vers '{log_file_path}'."); print(f"Vérifiez les permissions de stockage pour Pydroid 3 dans les paramètres Android."); print(f"Erreur détaillée: {e}")
            PokerMindCoachApp.log_file_handle = None

        # --- Build UI ---
        self.selected_adversaires = None; self.selected_position = None; self.analysis_event = None
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        with layout.canvas.before: Color(0.2, 0.3, 0.4, 1); self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.update_rect, pos=self.update_rect)
        app_scroll_view = ScrollView(size_hint=(1, 1))
        container = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(15), size_hint_y=None)
        container.bind(minimum_height=container.setter('height'))
        self.container = container
        def update_container_width(scroll_view_instance, scroll_view_width): self.container.width = scroll_view_width
        app_scroll_view.bind(width=update_container_width)

        # --- Sections with Spinners (Using CUSTOM_FONT_NAME) ---
        container.add_widget(Label(text="Votre Main", size_hint_y=None, height=dp(30), font_size='18sp'))
        main_spinners_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=dp(10))
        self.spinner_main1 = Spinner(text='Carte 1 : ?', values=self.CARD_NAMES, size_hint=(1, 1), font_name=CUSTOM_FONT_NAME) # Use custom font name
        self.spinner_main1.bind(text=self.on_card_select)
        main_spinners_layout.add_widget(self.spinner_main1)
        self.spinner_main2 = Spinner(text='Carte 2 : ?', values=self.CARD_NAMES, size_hint=(1, 1), font_name=CUSTOM_FONT_NAME) # Use custom font name
        self.spinner_main2.bind(text=self.on_card_select)
        main_spinners_layout.add_widget(self.spinner_main2)
        container.add_widget(main_spinners_layout)
        container.add_widget(Label(text="Flop", size_hint_y=None, height=dp(30), font_size='18sp'))
        flop_spinners_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=dp(10))
        self.spinner_flop1 = Spinner(text='Flop 1 : ?', values=self.CARD_NAMES, size_hint=(1, 1), font_name=CUSTOM_FONT_NAME) # Use custom font name
        self.spinner_flop1.bind(text=self.on_card_select)
        flop_spinners_layout.add_widget(self.spinner_flop1)
        self.spinner_flop2 = Spinner(text='Flop 2 : ?', values=self.CARD_NAMES, size_hint=(1, 1), font_name=CUSTOM_FONT_NAME) # Use custom font name
        self.spinner_flop2.bind(text=self.on_card_select)
        flop_spinners_layout.add_widget(self.spinner_flop2)
        self.spinner_flop3 = Spinner(text='Flop 3 : ?', values=self.CARD_NAMES, size_hint=(1, 1), font_name=CUSTOM_FONT_NAME) # Use custom font name
        self.spinner_flop3.bind(text=self.on_card_select)
        flop_spinners_layout.add_widget(self.spinner_flop3)
        container.add_widget(flop_spinners_layout)

        # --- Options Rows (Keep same) ---
        container.add_widget(Label(size_hint_y=None, height=dp(10)))
        container.add_widget(Label(text="Nombre d'adversaires", size_hint_y=None, height=dp(30), font_size='16sp'))
        self.adversaires_layout = self.create_option_row('Adversaires', ['1', '2', '3', '4', '5+'])
        container.add_widget(self.adversaires_layout)
        container.add_widget(Label(text="Votre Position", size_hint_y=None, height=dp(30), font_size='16sp'))
        self.position_layout = self.create_option_row('Position', ['Précoce', 'Milieu', 'Tardive', 'Blinds'])
        container.add_widget(self.position_layout)

        # --- Final Layout (Keep same) ---
        app_scroll_view.add_widget(container); layout.add_widget(app_scroll_view)
        self.analyse_button = Button(text="Analyser la main", size_hint=(1, None), height=dp(50), font_size='20sp', background_normal='', background_color=(0.2, 0.6, 0.3, 1), color=(1, 1, 1, 1), bold=True)
        self.analyse_button.bind(on_press=self.start_analysis_visuals); layout.add_widget(self.analyse_button)
        self.progress_bar = ProgressBar(max=100, value=0, size_hint=(1, None), height=dp(10)); layout.add_widget(self.progress_bar)
        self.result_label = Label(text="Conseil : Sélectionnez vos cartes et options.", size_hint=(1, None), height=dp(100), font_size='18sp', color=(0.9, 0.9, 0.9, 1), bold=True, text_size=(Window.width * 0.9 if Window.width else dp(300), None), valign='top', halign='center')
        Window.bind(width=self.update_label_text_size); layout.add_widget(self.result_label)

        print("DEBUG: Build method finished.")
        return layout

    # --- on_stop (Keep same) ---
    def on_stop(self):
        print(f"--- Log arrêté ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---")
        if PokerMindCoachApp.log_file_handle:
            original_stdout = sys.__stdout__; original_stderr = sys.__stderr__;
            try:
                sys.stdout = original_stdout; sys.stderr = original_stderr;
                PokerMindCoachApp.log_file_handle.close(); print("Fichier log fermé (on_stop).")
                PokerMindCoachApp.log_file_handle = None
            except Exception as e: print(f"Erreur en fermant le fichier log: {e}", file=original_stderr)
        else: print("INFO: Log handle était None dans on_stop, pas de fichier à fermer.", file=sys.__stdout__)

    # --- Other Methods (Keep same) ---
    def update_label_text_size(self, instance, width):
        if self.result_label: self.result_label.text_size = (width * 0.9, None)

    def on_card_select(self, spinner_instance, selected_name):
        print(f"DEBUG Spinner: '{selected_name}' sélectionné")
        selected_id = None;
        for card_id, card_name in self.CARDS_ID_TO_NAME.items():
            if card_name == selected_name: selected_id = card_id; break
        if spinner_instance == self.spinner_main1: self.hand_card1 = selected_id if selected_id else '?'
        elif spinner_instance == self.spinner_main2: self.hand_card2 = selected_id if selected_id else '?'
        elif spinner_instance == self.spinner_flop1: self.flop_card1 = selected_id if selected_id else '?'
        elif spinner_instance == self.spinner_flop2: self.flop_card2 = selected_id if selected_id else '?'
        elif spinner_instance == self.spinner_flop3: self.flop_card3 = selected_id if selected_id else '?'
        print(f"  -> IDs: Main=({self.hand_card1},{self.hand_card2}) Flop=({self.flop_card1},{self.flop_card2},{self.flop_card3})")

    def create_option_row(self, label, options):
        box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(45), spacing=dp(10))
        for option in options: btn = ToggleButton(text=option, group=label.lower(), size_hint=(1, 1), font_size='14sp', background_normal='', background_color=(0.3, 0.3, 0.3, 1), background_down='', background_disabled_normal = '', color=(1, 1, 1, 1), border=(dp(5),)*4); btn.bind(state=lambda instance, value, lbl=label, opt=option: self.on_toggle_select(instance, value, lbl, opt)); box.add_widget(btn)
        return box

    def on_toggle_select(self, button, state, label, option):
        if state == 'down': button.background_color = (0.4, 0.6, 0.8, 1);
        if label == 'Adversaires': self.selected_adversaires = option;
        elif label == 'Position': self.selected_position = option
        else: button.background_color = (0.3, 0.3, 0.3, 1)
        if state == 'normal':
             if label == 'Adversaires' and self.selected_adversaires == option: self.selected_adversaires = None
             elif label == 'Position' and self.selected_position == option: self.selected_position = None

    def start_analysis_visuals(self, instance):
        error_msg = ""; selected_hand = [self.hand_card1, self.hand_card2]; selected_flop = [self.flop_card1, self.flop_card2, self.flop_card3]
        actual_hand = [c for c in selected_hand if c != '?']; actual_flop = [c for c in selected_flop if c != '?']
        if len(actual_hand) != 2: error_msg += f"Sélectionnez exactement 2 cartes pour votre main (actuellement {len(actual_hand)}).\n"
        if len(actual_flop) != 3: error_msg += f"Sélectionnez exactement 3 cartes pour le flop (actuellement {len(actual_flop)}).\n"
        all_selected_cards = actual_hand + actual_flop
        if len(all_selected_cards) != len(set(all_selected_cards)): error_msg += "Vous avez sélectionné la même carte plusieurs fois.\n"
        if not self.selected_adversaires: error_msg += "Sélectionnez le nombre d'adversaires.\n"
        if not self.selected_position: error_msg += "Sélectionnez votre position.\n"
        if error_msg:
             self.result_label.text = f"Erreur : \n{error_msg.strip()}"; self.progress_bar.value = 0; self.analyse_button.disabled = False
             if self.analysis_event: self.analysis_event.cancel(); self.analysis_event = None
             return
        self.analyse_button.disabled = True; self.progress_bar.value = 0; self.result_label.text = "Analyse en cours..."
        if self.analysis_event: self.analysis_event.cancel()
        self.analysis_event = Clock.schedule_interval(self.update_progress, 0.02)

    def update_progress(self, dt):
        if self.progress_bar.value < 100: self.progress_bar.value += 2
        else:
            if self.analysis_event: self.analysis_event.cancel(); self.analysis_event = None
            self.analyser()

    def analyser(self):
        main_ids_list = [self.hand_card1, self.hand_card2]; flop_ids_list = [self.flop_card1, self.flop_card2, self.flop_card3]
        try:
            adv_text = self.selected_adversaires;
            if adv_text is None: raise ValueError("Nombre d'adversaires non sélectionné.")
            num_adversaires = 5 if adv_text == '5+' else int(adv_text)
            if '?' in main_ids_list or '?' in flop_ids_list: raise ValueError("Toutes les cartes n'ont pas été sélectionnées.")
            conseil = self.analyser_logique(main_ids_list, flop_ids_list, num_adversaires, self.selected_position)
            self.result_label.text = f"Conseil : {conseil}"
        except ValueError as ve: self.result_label.text = f"Erreur: {str(ve)}"; print(f"Erreur (ValueError) détaillée: {ve}", flush=True)
        except Exception as e: self.result_label.text = f"Erreur d'analyse : {str(e)}"; print(f"Erreur d'analyse détaillée: {e}", flush=True)
        finally:
            self.analyse_button.disabled = False
            if self.analysis_event: self.analysis_event.cancel(); self.analysis_event = None

    def analyser_logique(self, main_cards, flop_cards, num_adversaires, position):
        # (Keep previous clean version)
        rank_map = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '0': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}; value_map = {v: k for k, v in rank_map.items()}
        try: main_parsed = [{'id': c, 'rank': rank_map[c[0]], 'suit': c[1]} for c in main_cards]; flop_parsed = [{'id': c, 'rank': rank_map[c[0]], 'suit': c[1]} for c in flop_cards]
        except KeyError as e: raise ValueError(f"Carte invalide ('{str(e)}'). Vérifiez sélections.") from e
        all_cards = main_parsed + flop_parsed; all_ranks = sorted([c['rank'] for c in all_cards], reverse=True); all_suits = [c['suit'] for c in all_cards]; main_ranks = sorted([c['rank'] for c in main_parsed], reverse=True); main_suits = [c['suit'] for c in main_parsed]; flop_ranks = sorted([c['rank'] for c in flop_parsed], reverse=True); flop_suits = [c['suit'] for c in flop_parsed]
        conseils = []; is_pair_in_hand = main_ranks[0] == main_ranks[1]; is_suited_hand = main_suits[0] == main_suits[1]; is_connector = abs(main_ranks[0] - main_ranks[1]) == 1 or set(main_ranks) == {14, 2}
        if is_pair_in_hand: pair_rank_val = main_ranks[0]; pair_rank_str = value_map[pair_rank_val];
        if pair_rank_val >= rank_map['J']: conseils.append(f"Grosse paire en main ({pair_rank_str * 2})")
        elif pair_rank_val >= rank_map['7']: conseils.append(f"Paire moyenne en main ({pair_rank_str * 2})")
        else: conseils.append(f"Petite paire en main ({pair_rank_str * 2})")
        if is_suited_hand: conseils.append("Main assortie");
        if is_connector: conseils.append("Connecteurs en main");
        if max(main_ranks) >= rank_map['Q'] and not is_pair_in_hand: conseils.append("Hautes cartes en main")
        flop_suit_counts = {s: flop_suits.count(s) for s in set(flop_suits)}; is_flop_mono = any(count == 3 for count in flop_suit_counts.values()); is_flop_flush_draw = any(count == 2 for count in flop_suit_counts.values()); flop_rank_counts = {r: flop_ranks.count(r) for r in set(flop_ranks)}; is_flop_paired = any(count == 2 for count in flop_rank_counts.values()); is_flop_trips = any(count == 3 for count in flop_rank_counts.values()); is_flop_straight_possible = False
        if len(set(flop_ranks)) == 3: ranks_sorted = sorted(list(set(flop_ranks)));
        if ranks_sorted[2] - ranks_sorted[0] == 2: is_flop_straight_possible = True
        elif set(ranks_sorted) == {14, 2, 3}: is_flop_straight_possible = True
        if is_flop_trips: conseils.append("Brelan sur le flop")
        elif is_flop_paired: conseils.append("Flop pairé")
        if is_flop_mono: conseils.append("Flop monochrome")
        elif is_flop_flush_draw: conseils.append("Tirage couleur sur flop (2 cartes)")
        if is_flop_straight_possible: conseils.append("Flop connecté (tirage suite)")
        rank_counts = {r: all_ranks.count(r) for r in set(all_ranks)}; suit_counts = {s: all_suits.count(s) for s in set(all_suits)}; hand_rank_values = list(rank_counts.values()); unique_ranks = sorted(list(set(all_ranks)), reverse=True); made_hand = ""; is_flush = any(count >= 5 for count in suit_counts.values()); flush_suit = [s for s, count in suit_counts.items() if count >= 5];
        is_straight = False; straight_high_card = -1
        if len(unique_ranks) >= 5:
             for i in range(len(unique_ranks) - 4):
                 sub_seq = unique_ranks[i:i+5]
                 if sub_seq[0] - sub_seq[4] == 4: is_straight = True; straight_high_card = sub_seq[0]; break
             if not is_straight and set(unique_ranks).issuperset({14, 2, 3, 4, 5}): is_straight = True; straight_high_card = 5
        is_straight_flush = False
        if is_flush and is_straight: flush_cards_ranks = sorted([c['rank'] for c in all_cards if c['suit'] == flush_suit[0]], reverse=True);
        if len(flush_cards_ranks) >= 5:
             for i in range(len(flush_cards_ranks) - 4):
                 sub_seq = flush_cards_ranks[i:i+5];
                 if sub_seq[0] - sub_seq[4] == 4: is_straight_flush = True; break
             if not is_straight_flush and set(flush_cards_ranks).issuperset({14, 2, 3, 4, 5}): is_straight_flush = True; straight_high_card = 5
        if is_straight_flush: made_hand = f"Quinte Flush ({value_map.get(straight_high_card, '?')} haute)"
        elif 4 in hand_rank_values: four_kind_rank = [r for r, count in rank_counts.items() if count == 4][0]; made_hand = f"Carré de {value_map[four_kind_rank]}"
        elif sorted(hand_rank_values, reverse=True)[:2] == [3, 2]: three_kind_rank = [r for r, count in rank_counts.items() if count == 3][0]; pair_rank = [r for r, count in rank_counts.items() if count == 2][0]; made_hand = f"Full House ({value_map[three_kind_rank]} par les {value_map[pair_rank]})"
        elif is_flush: flush_high_card = max([c['rank'] for c in all_cards if c['suit'] == flush_suit[0]]); made_hand = f"Couleur ({value_map[flush_high_card]} haute)"
        elif is_straight: made_hand = f"Suite ({value_map.get(straight_high_card, '?')} haute)"
        elif 3 in hand_rank_values: three_kind_rank = [r for r, count in rank_counts.items() if count == 3][0]; made_hand = f"Brelan de {value_map[three_kind_rank]}"
        elif hand_rank_values.count(2) >= 2: pairs_ranks = sorted([r for r, count in rank_counts.items() if count == 2], reverse=True); made_hand = f"Deux Paires ({value_map[pairs_ranks[0]]} et {value_map[pairs_ranks[1]]})"
        elif 2 in hand_rank_values: pair_rank = [r for r, count in rank_counts.items() if count == 2][0]; made_hand = f"Paire de {value_map[pair_rank]}"
        else: made_hand = f"Hauteur {value_map[all_ranks[0]]}"
        force = 0
        if "Quinte Flush" in made_hand: force = 9
        elif "Carré" in made_hand: force = 8
        elif "Full House" in made_hand: force = 7
        elif "Couleur" in made_hand: force = 6
        elif "Suite" in made_hand: force = 5
        elif "Brelan" in made_hand: force = 4
        elif "Deux Paires" in made_hand: force = 3
        elif "Paire" in made_hand: force = 2
        elif "Hauteur" in made_hand: force = 1
        action = "Check/Fold"
        if force >= 7: action = "Miser Fort / Relancer"
        elif force >= 5: action = "Miser / Relancer"
        elif force >= 3: action = "Miser petit / Suivre"
        elif force >= 2: action = "Check / Suivre petite mise"
        else: action = "Check/Fold sauf si gratuit"
        if position in ['Tardive', 'Blinds'] and num_adversaires <= 2 and force >= 1:
            if action in ["Check/Fold", "Check / Suivre petite mise"]: action = "Tentative de Vol (petite mise)"
        elif position in ['Précoce'] and num_adversaires >= 4 and force <= 3:
             if action not in ["Miser Fort / Relancer", "Miser / Relancer"]: action = "Jouer très prudemment / Fold"
        observations_str = ". ".join(conseils)
        if observations_str: observations_str += ". "
        final_conseil = f"{observations_str}Force: {made_hand}. -> Action: {action}"
        return final_conseil.replace("..", ".").strip()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# --- Point d'entrée ---
if __name__ == '__main__':
    PokerMindCoachApp().run()
