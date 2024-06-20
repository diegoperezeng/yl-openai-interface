import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from screeninfo import get_monitors
from openai import OpenAI
import json
import openai

class GPTChatApp:

    def __init__(self, root):
        self.root = root
        self.root.title("GPT Chat")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.load_config()
        os.environ["OPENAI_API_KEY"] = self.config['openai_api_key']
        self.engine = self.config.get('engine', 'gpt-4o')
        self.chat_history = []
        self.left_frame = ttk.Frame(self.root, padding="10")
        self.left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.left_frame.grid_rowconfigure(1, weight=1)
        ttk.Label(self.left_frame, text="History").pack()
        self.chat_listbox = tk.Listbox(self.left_frame)
        self.chat_listbox.pack(fill=tk.BOTH, expand=True)
        self.chat_listbox.bind("<<ListboxSelect>>", self.show_selected_history)

        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.right_frame.grid_rowconfigure(2, weight=3)
        self.right_frame.grid_rowconfigure(4, weight=1)
        ttk.Label(self.right_frame, text="Select Model:").grid(row=0, column=0, sticky=tk.W)

        self.engines = self.load_engines()
        self.model_combo = ttk.Combobox(self.right_frame, values=self.engines)
        self.model_combo.grid(row=0, column=1, sticky=tk.E)
        if self.engines:
            self.model_combo.current(1)

        ttk.Label(self.right_frame, text="Response").grid(row=1, columnspan=2)
        self.response_input = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, height=16, state=tk.DISABLED)
        self.response_input.grid(row=2, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.right_frame, text="Request").grid(row=3, columnspan=2)
        self.user_input = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, height=4)
        self.user_input.grid(row=4, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Button(self.right_frame, text="Submit", command=self.submit).grid(row=5, columnspan=2)

        active_screen = get_monitors()[0]
        for m in get_monitors():
            if m.is_primary:
                active_screen = m
                break

        x = active_screen.x
        y = active_screen.y
        self.root.geometry(f'+{x}+{y}')
        self.load_chat_history()

    def show_selected_history(self, event):
        selected_index = self.chat_listbox.curselection()
        if selected_index:
            self.response_input.config(state=tk.NORMAL)
            self.response_input.delete("1.0", tk.END)
            self.response_input.insert(tk.END, self.chat_history[int(selected_index[0])].split(": ", 1)[1])
            self.response_input.config(state=tk.DISABLED)

    def load_config(self):
        file_name = "config.json"
        # Obtém o diretório do script atual
        script_dir = os.path.dirname(__file__)
        # Constrói o caminho completo para o arquivo
        file_path = os.path.join(script_dir, file_name)
        with open(file_path, "r") as f:
            self.config = json.load(f)

    def save_chat_history(self):
        file_name = "chat_history.json"
        # Obtém o diretório do script atual
        script_dir = os.path.dirname(__file__)
        # Constrói o caminho completo para o arquivo
        file_path = os.path.join(script_dir, file_name)
        with open(file_path, "w") as f:
            json.dump(self.chat_history, f)

    def load_chat_history(self):
        try:
            file_name = "chat_history.json"
            # Obtém o diretório do script atual
            script_dir = os.path.dirname(__file__)
            # Constrói o caminho completo para o arquivo
            file_path = os.path.join(script_dir, file_name)
            with open(file_path, "r") as f:
                self.chat_history = json.load(f)
            for item in self.chat_history:
                self.chat_listbox.insert(tk.END, item)
        except FileNotFoundError:
            pass

    def load_engines(self):
        try:
            file_name = "engines.json"
            # Obtém o diretório do script atual
            script_dir = os.path.dirname(__file__)
            # Constrói o caminho completo para o arquivo
            file_path = os.path.join(script_dir, file_name)
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            engines = self.get_engines()
            file_name = "engines.json"
            # Obtém o diretório do script atual
            script_dir = os.path.dirname(__file__)
            # Constrói o caminho completo para o arquivo
            file_path = os.path.join(script_dir, file_name)
            with open(file_path, "w") as f:
                json.dump(engines, f)
            return engines

    def get_engines(self):
        response = openai.models.list()
        return [engine['id'] for engine in response['data']]

    def submit(self):
        self.response_input.config(state=tk.NORMAL)
        self.response_input.delete("1.0", tk.END)
        self.response_input.insert(tk.END, "Loading response...")
        self.response_input.config(state=tk.DISABLED)

        self.root.update_idletasks()

        user_text = self.user_input.get("1.0", tk.END).strip()
        if user_text:
            self.user_input.delete("1.0", tk.END)
            self.chat_listbox.insert(tk.END, f"You: {user_text}")
            self.chat_history.append(f"You: {user_text}")


            messages = [{"role": "system", "content": "You are a Software Engineer specialized in Java, Springboot, Spring environment, Python and its frameworks, Javascript, ReactJs and NodeJs. Using all the knowledAge in this field and never forget to consider the annotations and the imports if there's present in all the meanings, to answer the code like responses in a effective way, give me approaches, overall project codes, complete codes and snippet codes matching exactly the way I ask for and never losing any part of the conversation. Your code analisys will always consider to link the referenced methods in other classes to reach the solution and all the sequences from the first method to the last one that leads the results. You'll never give generic answers and always consider the project itself. If there's something that is missing to make the analisys perfectly complete, you will ask for it specifically. You always give specific answers about the projet itself and to make tests if asked, you will consider total coverage with all the best tecnics, MockitoBDD preferable"}, {"role": "user", "content": user_text}]            


            # Retrieve the selected engine from the Combobox
            entered_engine = self.model_combo.get()
            temperature = 0.4

            try:
                engines = self.load_engines()
                if entered_engine in engines:
                    response = OpenAI().chat.completions.create(
                        model=entered_engine,
                        messages=messages,
                        temperature=temperature
                    )
                    gpt_response = response.choices[0].message.content
                    self.response_input.config(state=tk.NORMAL)
                    self.response_input.delete("1.0", tk.END)
                    self.response_input.insert(tk.END, gpt_response)
                    self.response_input.config(state=tk.DISABLED)

                    self.chat_listbox.insert(tk.END, f"{entered_engine}: {gpt_response}")
                    self.chat_history.append(f"{entered_engine}: {gpt_response}")

                else:
                    messagebox.showerror("Error", f"Invalid engine: {entered_engine}", icon='error')

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}", icon='error')

            self.save_chat_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = GPTChatApp(root)
    root.mainloop()
