import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from PIL import Image, ImageTk
from io import BytesIO

try:
    lanczos = Image.Resampling.LANCZOS
except AttributeError:
    lanczos = Image.LANCZOS  # type: ignore

class HPCharacter:
    
    def __init__(self, data):
        self.id = data.get('id', '')
        self.name = data.get('name', 'Unknown')
        self.alternate_names = data.get('alternate_names', [])
        self.species = data.get('species', 'Unknown')
        self.gender = data.get('gender', 'Unknown')
        self.house = data.get('house', 'Unknown')
        self.dateOfBirth = data.get('dateOfBirth', 'Unknown')
        self.ancestry = data.get('ancestry', 'Unknown')
        self.eyeColour = data.get('eyeColour', 'Unknown')
        self.hairColour = data.get('hairColour', 'Unknown')
        self.wand = data.get('wand', {})
        self.patronus = data.get('patronus', 'Unknown')
        self.actor = data.get('actor', 'Unknown')
        self.image = data.get('image', '')
        self.alive = data.get('alive', True)
    
    def get_wand_info(self):
        if not self.wand or not any(self.wand.values()):
            return "Unknown"
        wood = self.wand.get('wood', 'Unknown')
        core = self.wand.get('core', 'Unknown')
        length = self.wand.get('length', 'Unknown')
        return f"{wood} wood, {core} core, {length} inches" if length != 'Unknown' else f"{wood} wood, {core} core"
    
    def get_alternate_names_text(self):
        if not self.alternate_names:
            return "None"
        return ", ".join(self.alternate_names)


class HPSpell:
    
    def __init__(self, data):
        self.id = data.get('id', '')
        self.name = data.get('name', 'Unknown')
        self.description = data.get('description', 'No description available')


class HarryPotterAPI:
    
    BASE_URL = "https://hp-api.onrender.com/api"
    
    @staticmethod
    def get_all_characters():
        try:
            response = requests.get(f"{HarryPotterAPI.BASE_URL}/characters", timeout=10)
            response.raise_for_status()
            data = response.json()
            return [HPCharacter(char) for char in data]
        except Exception as e:
            raise Exception(f"Error fetching characters: {str(e)}")
    
    @staticmethod
    def get_students():
        try:
            response = requests.get(f"{HarryPotterAPI.BASE_URL}/characters/students", timeout=10)
            response.raise_for_status()
            data = response.json()
            return [HPCharacter(char) for char in data]
        except Exception as e:
            raise Exception(f"Error fetching students: {str(e)}")
    
    @staticmethod
    def get_staff():
        try:
            response = requests.get(f"{HarryPotterAPI.BASE_URL}/characters/staff", timeout=10)
            response.raise_for_status()
            data = response.json()
            return [HPCharacter(char) for char in data]
        except Exception as e:
            raise Exception(f"Error fetching staff: {str(e)}")
    
    @staticmethod
    def get_house_characters(house):
        try:
            response = requests.get(f"{HarryPotterAPI.BASE_URL}/characters/house/{house.lower()}", timeout=10)
            response.raise_for_status()
            data = response.json()
            return [HPCharacter(char) for char in data]
        except Exception as e:
            raise Exception(f"Error fetching house characters: {str(e)}")
    
    @staticmethod
    def get_spells():
        try:
            response = requests.get(f"{HarryPotterAPI.BASE_URL}/spells", timeout=10)
            response.raise_for_status()
            data = response.json()
            return [HPSpell(spell) for spell in data]
        except Exception as e:
            raise Exception(f"Error fetching spells: {str(e)}")


class HarryPotterApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Harry Potter Club-House")
        self.root.geometry("1000x750")
        self.root.configure(bg='#1a1a2e')
        self.root.minsize(1000, 750)  
        
        self.hp_api = HarryPotterAPI()
        
        self.current_image = None
        self.current_hp_items = []
        self.current_hp_type = 'character'
        
        self.setup_ui()
        
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(fill='both', expand=True, padx=10, pady=(10, 5))
        
        title_frame = tk.Frame(main_container, bg='#16213e', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="Harry Potter Club-House 🪄", 
            font=('Harry Potter Font', 24, 'bold'),
            bg="#16213e",
            fg="#9e78d2"
        )
        title_label.pack(expand=True)
        
        content_frame = tk.Frame(main_container, bg='#1a1a2e')
        content_frame.pack(fill='both', expand=True)
        
        left_panel = tk.Frame(content_frame, bg='#0f3460', width=300)
        left_panel.pack(side='left', fill='both', expand=False, padx=(0, 5))
        
        search_frame = tk.LabelFrame(left_panel, text="Browse Options", bg='#0f3460', fg="#5bc3e6", 
                                   font=('Arial', 11, 'bold'), padx=10, pady=10)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(search_frame, text="All Characters", command=self.get_all_hp_characters,
                 bg="#651321", fg='white', font=('Arial', 10, 'bold'), cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(search_frame, text="Students Only", command=self.get_hp_students,
                 bg='#651321', fg='white', font=('Arial', 10, 'bold'), cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(search_frame, text="Staff Only", command=self.get_hp_staff,
                 bg='#651321', fg='white', font=('Arial', 10, 'bold'), cursor='hand2').pack(fill='x', pady=2)

        tk.Label(search_frame, text="Filter by House:", bg='#0f3460', fg="#56c3e8", pady=10).pack(anchor='w')
        self.hp_house_var = tk.StringVar()
        houses = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']
        self.hp_house_combo = ttk.Combobox(search_frame, textvariable=self.hp_house_var, 
                                        values=houses, state='readonly')
        self.hp_house_combo.pack(fill='x', pady=(0, 5))
        self.hp_house_combo.current(0)
        
        tk.Button(search_frame, text="Filter by House", command=self.filter_hp_by_house,
                 bg="#085159", fg='white', font=('Arial', 10, 'bold'), cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(search_frame, text="✨ View All Spells", command=self.get_hp_spells,
                 bg='#533483', fg='white', font=('Arial', 10, 'bold'), cursor='hand2').pack(fill='x', pady=(10, 2))
        
        results_frame = tk.LabelFrame(left_panel, text="Results", bg='#0f3460', fg="#74a6c6",
                                    font=('Arial', 11, 'bold'), padx=10, pady=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(results_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.hp_results_listbox = tk.Listbox(results_frame, font=('Arial', 10), bg="#addae5",
                                          selectmode='single', yscrollcommand=scrollbar.set, height=15)
        self.hp_results_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.hp_results_listbox.yview)
        self.hp_results_listbox.bind('<<ListboxSelect>>', self.on_hp_select)
        
        right_panel = tk.Frame(content_frame, bg='#0f3460')
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        details_frame = tk.LabelFrame(right_panel, text="Character/Spell Details", bg='#0f3460', fg="#5ec6e0",
                                    font=('Arial', 11, 'bold'), padx=10, pady=10)
        details_frame.pack(fill='both', expand=True)
        
        self.hp_image_label = tk.Label(details_frame, bg='#0f3460')
        self.hp_image_label.pack(pady=10)
        
        self.hp_details_text = scrolledtext.ScrolledText(details_frame, font=('Arial', 10),
                                                      bg="#b0e3f0", wrap='word', height=20)
        self.hp_details_text.pack(fill='both', expand=True, pady=5)
        
        self.status_label = tk.Label(
            self.root,
            text="Welcome to Harry Potter Club.",
            bg='#1a0033',
            fg="#ffd700",
            anchor='w',
            padx=10,
            height=2
        )
        self.status_label.pack(fill='x', side='bottom', pady=(0, 10))
    
    def get_all_hp_characters(self):
        self.update_status("Loading all characters...")
        try:
            self.current_hp_items = self.hp_api.get_all_characters()
            self.current_hp_type = 'character'
            self.display_hp_results()
            self.update_status(f"Loaded {len(self.current_hp_items)} characters")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Failed to load characters")
    
    def get_hp_students(self):
        self.update_status("Loading students...")
        try:
            self.current_hp_items = self.hp_api.get_students()
            self.current_hp_type = 'character'
            self.display_hp_results()
            self.update_status(f"Loaded {len(self.current_hp_items)} students")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Failed to load students")
    
    def get_hp_staff(self):
        self.update_status("Loading staff...")
        try:
            self.current_hp_items = self.hp_api.get_staff()
            self.current_hp_type = 'character'
            self.display_hp_results()
            self.update_status(f"Loaded {len(self.current_hp_items)} staff members")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Failed to load staff")
    
    def filter_hp_by_house(self):
        house = self.hp_house_var.get()
        if not house:
            messagebox.showwarning("Selection Required", "Please select a house")
            return
        
        self.update_status(f"Loading {house} members...")
        try:
            self.current_hp_items = self.hp_api.get_house_characters(house)
            self.current_hp_type = 'character'
            self.display_hp_results()
            self.update_status(f"Loaded {len(self.current_hp_items)} {house} members")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Failed to filter by house")
    
    def get_hp_spells(self):
        self.update_status("Loading spells...")
        try:
            self.current_hp_items = self.hp_api.get_spells()
            self.current_hp_type = 'spell'
            self.display_hp_results()
            self.update_status(f"Loaded {len(self.current_hp_items)} spells")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Failed to load spells")
    
    def display_hp_results(self):
        self.hp_results_listbox.delete(0, tk.END)
        
        if not self.current_hp_items:
            self.hp_results_listbox.insert(tk.END, "No results found")
            self.clear_hp_details()
            return
        
        for item in self.current_hp_items:
            self.hp_results_listbox.insert(tk.END, item.name)
    
    def on_hp_select(self, event):
        selection = self.hp_results_listbox.curselection()
        if not selection or not hasattr(self, 'current_hp_items') or not self.current_hp_items:
            return
        
        index = selection[0]
        item = self.current_hp_items[index]
        
        if self.current_hp_type == 'character':
            self.display_hp_character_details(item)
        else:
            self.display_hp_spell_details(item)
    
    def display_hp_character_details(self, character):
        self.update_status("Loading character details...")
        
        self.hp_details_text.delete('1.0', tk.END)
        
        details = f"{character.name}\n"
        details += "=" * 60 + "\n\n"
        details += f"House: {character.house}\n"
        details += f"Species: {character.species}\n"
        details += f"Gender: {character.gender}\n"
        details += f"Date of Birth: {character.dateOfBirth}\n"
        details += f"Ancestry: {character.ancestry}\n"
        details += f"Eye Colour: {character.eyeColour}\n"
        details += f"Hair Colour: {character.hairColour}\n"
        details += f"Wand: {character.get_wand_info()}\n"
        details += f"Patronus: {character.patronus}\n"
        details += f"Actor: {character.actor}\n"
        details += f"Status: {'Alive' if character.alive else 'Deceased'}\n"
        details += f"\nAlternate Names: {character.get_alternate_names_text()}\n"
        
        self.hp_details_text.insert('1.0', details)
        
        if character.image:
            self.load_image(character.image, self.hp_image_label)
        else:
            self.hp_image_label.config(image='', text="No image available")
        
        self.update_status("Character details loaded")
    
    def display_hp_spell_details(self, spell):
        self.update_status("Loading spell details...")
        
        self.hp_details_text.delete('1.0', tk.END)
        
        details = f"✨ {spell.name} ✨\n"
        details += "=" * 60 + "\n\n"
        details += f"Description:\n{spell.description}\n"
        
        self.hp_details_text.insert('1.0', details)
        
        self.hp_image_label.config(image='', text="⚡")
        self.hp_image_label.config(font=('Arial', 48))
        
        self.update_status("Spell details loaded")
    
    def clear_hp_details(self):
        self.hp_details_text.delete('1.0', tk.END)
        self.hp_image_label.config(image='', text="", font=('Arial', 10))
    
    def load_image(self, url, label):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            image_data = Image.open(BytesIO(response.content))
            image_data = image_data.resize((250, 250), lanczos)
            self.current_image = ImageTk.PhotoImage(image_data)
            label.config(image=self.current_image, text="")
        except Exception as e:
            label.config(image='', text="Image not available")
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = HarryPotterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()