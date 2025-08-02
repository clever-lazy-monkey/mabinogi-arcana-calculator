import tkinter as tk
from tkinter import ttk, messagebox
from math import ceil

# arcana level calculator
def arcana_level_calculator():
    arcana_levels = [
        (1, 0), (2, 600), (3, 1206), (4, 1818), (5, 2463),
        (6, 3060), (7, 3690), (8, 4326), (9, 4968), (10, 5040),
        (11, 6276), (12, 6949), (13, 7635), (14, 8334), (15, 9046),
        (16, 9772), (17, 10512), (18, 11266), (19, 12035), (20, 12819),
        (21, 13626), (22, 14457), (23, 15312), (24, 16192), (25, 17098),
        (26, 18031), (27, 18991), (28, 19979), (29, 20996), (30, 22043),
        (31, 23131), (32, 24262), (33, 25438), (34, 26661), (35, 27932),
        (36, 29253), (37, 30626), (38, 32053), (39, 33537), (40, 35080),
        (41, 36700), (42, 38401), (43, 40187), (44, 42062), (45, 44030),
        (46, 46096), (47, 48265), (48, 50542), (49, 52932), (50, 55441)
    ]
    
    def calculate_progress(current_level=None, current_exp=None):
        max_exp = 55441
        
        if current_exp is not None and current_level is None:
            inferred_level = 1
            for lvl, exp_required in arcana_levels:
                if current_exp >= exp_required:
                    inferred_level = lvl
                else:
                    break
            current_level = inferred_level
        
        if current_level is not None and current_exp is None:
            current_exp = arcana_levels[current_level-1][1]
        
        if current_level < 1 or current_level > 50:
            return "Error: Level must be between 1 and 50"
        if current_exp < arcana_levels[current_level-1][1]:
            return "Error: Current EXP is less than required for your level"
        
        if current_level == 50:
            exp_to_next = 0
            exp_in_level = current_exp - arcana_levels[current_level-1][1]
        else:
            current_level_exp = arcana_levels[current_level-1][1]
            next_level_exp = arcana_levels[current_level][1]
            exp_to_next = next_level_exp - current_level_exp
            exp_in_level = current_exp - current_level_exp
        
        progress_percent = (exp_in_level / exp_to_next) * 100 if exp_to_next > 0 else 100
        
        exp_left = max_exp - current_exp
        levels_left = 50 - current_level
        level_ups_needed = (exp_left + 14) // 15
        
        exact_rebirths = level_ups_needed / 200
        rounded_rebirths = ceil(exact_rebirths)
        
        return {
            "current_level": current_level,
            "current_exp": current_exp,
            "exp_in_current_level": exp_in_level,
            "exp_to_next_level": exp_to_next,
            "progress_percent": round(progress_percent, 1),
            "exp_left_to_max": exp_left,
            "levels_left_to_max": levels_left,
            "level_ups_needed": level_ups_needed,
            "rebirths_needed": f"~{rounded_rebirths} (exact: {round(exact_rebirths, 1)})"
        }
    
    return calculate_progress

# crest/thread calculator
def arcana_crest_calculator():
    link_stages = [
        (1, 10, 60, 50, 50, 0, 0),
        (2, 20, 130, 75, 125, 0, 0),
        (3, 30, 210, 125, 250, 0, 0),
        (4, 40, 300, 200, 450, 0, 0),
        (5, 50, 400, 300, 750, 0, 0),
        (6, 50, 120, 100, 850, 10, 10),
        (7, 50, 260, 150, 1000, 15, 25),
        (8, 50, 420, 250, 1250, 25, 50),
        (9, 50, 600, 400, 1650, 40, 90),
        (10, 50, 800, 600, 2250, 60, 150)
    ]
    
    def create_column_line(left_text, right_text, width=35):
        return f"{left_text.ljust(width)} | {right_text}"
    
    def calculate_crest_needs(current_stage, target_stage, current_scorching=0, current_ice=0, 
                            current_smoldering=0, current_frostflame=0):
        
        if current_stage < 0 or current_stage > 10 or target_stage < 0 or target_stage > 10:
            return "Error: Stages must be between 0 and 10"
        if current_stage >= target_stage:
            return "Error: Target stage must be higher than current stage"
        
        current_scorching_cumulative = link_stages[current_stage][4] if current_stage > 0 else 0
        current_ice_cumulative = link_stages[current_stage][6] if current_stage > 0 else 0
        
        target_scorching_cumulative = link_stages[target_stage - 1][4]
        target_ice_cumulative = link_stages[target_stage - 1][6]
        
        scorching_needed = target_scorching_cumulative - current_scorching_cumulative
        ice_needed = target_ice_cumulative - current_ice_cumulative
        
        total_scorching_owned = current_scorching + current_smoldering
        total_ice_owned = current_ice + current_frostflame
        
        scorching_to_get = max(0, scorching_needed - total_scorching_owned)
        ice_to_get = max(0, ice_needed - total_ice_owned)
        
        smoldering_to_buy = max(0, scorching_needed - current_scorching - current_smoldering)
        frostflame_to_buy = max(0, ice_needed - current_ice - current_frostflame)
        
        scorching_gold_cost = (current_smoldering + smoldering_to_buy) * 10000
        ice_gold_cost = (current_frostflame + frostflame_to_buy) * 150000
        
        if current_scorching > 0:
            scorching_gold_cost = max(0, scorching_gold_cost - (current_scorching * 10000))
        if current_ice > 0:
            ice_gold_cost = max(0, ice_gold_cost - (current_ice * 150000))
        
        return {
            "current_stage": current_stage,
            "target_stage": target_stage,
            "scorching_needed": scorching_needed,
            "ice_needed": ice_needed,
            "scorching_to_get": scorching_to_get,
            "ice_to_get": ice_to_get,
            "smoldering_to_buy": smoldering_to_buy,
            "frostflame_to_buy": frostflame_to_buy,
            "scorching_gold_cost": scorching_gold_cost,
            "ice_gold_cost": ice_gold_cost,
            "total_gold_cost": scorching_gold_cost + ice_gold_cost,
            "needs_ice": ice_needed > 0
        }
    
    return calculate_crest_needs

# gui windows
def open_arcana_window():
    calculate_progress = arcana_level_calculator()
    
    arcana_window = tk.Toplevel()
    arcana_window.title("🦍 Arcana Level Calculator")
    arcana_window.geometry("500x400")
    
    input_frame = ttk.Frame(arcana_window, padding="20")
    input_frame.pack(fill=tk.X)
    
    ttk.Label(input_frame, text="Current Arcana Level (1-50) (optional):").grid(row=0, column=0, sticky="w", pady=5)
    level_entry = ttk.Entry(input_frame, width=15)
    level_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(input_frame, text="Total Arcana EXP (optional):").grid(row=1, column=0, sticky="w", pady=5)
    exp_entry = ttk.Entry(input_frame, width=15)
    exp_entry.grid(row=1, column=1, padx=10, pady=5)
    
    calc_button = ttk.Button(input_frame, text="Calculate", 
                            command=lambda: calculate_arcana_gui(level_entry, exp_entry, result_text, calculate_progress))
    calc_button.grid(row=2, column=0, columnspan=2, pady=15)
    
    result_frame = ttk.Frame(arcana_window, padding="20")
    result_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(result_frame, text="Results:", font=('Arial', 12, 'bold')).pack(anchor="w")
    
    result_text = tk.Text(result_frame, height=15, width=60, font=('Arial', 10))
    result_text.pack(fill=tk.BOTH, expand=True, pady=10)
    
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_text.yview)
    scrollbar.pack(side="right", fill="y")
    result_text.configure(yscrollcommand=scrollbar.set)

def calculate_arcana_gui(level_entry, exp_entry, result_text, calculate_progress):
    try:
        level_input = level_entry.get().strip()
        exp_input = exp_entry.get().strip()
        
        current_level = int(level_input) if level_input else None
        current_exp = int(exp_input) if exp_input else None
        
        if current_level is None and current_exp is None:
            messagebox.showerror("Error", "You must enter at least a level OR exp value")
            return
        
        result = calculate_progress(current_level, current_exp)
        
        if isinstance(result, str):
            messagebox.showerror("Error", result)
            return
        
        result_text.delete(1.0, tk.END)
        
        exp_note = ""
        if current_level is not None and exp_input == "":
            exp_note = f" (using minimum EXP for level {current_level})"
        
        output = f"""=== 🐒 Results 🐵 ===
Current Level: {result['current_level']}
Current Total EXP: {result['current_exp']:,}{exp_note}
Progress in Level {result['current_level']}: {result['exp_in_current_level']}/{result['exp_to_next_level']} EXP ({result['progress_percent']}%)
EXP left to max (Level 50): {result['exp_left_to_max']:,}
Levels left to max: {result['levels_left_to_max']}
Level ups needed: {result['level_ups_needed']:,}
Rebirths needed (200 levels each): {result['rebirths_needed']}"""
        
        result_text.insert(tk.END, output)
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def open_crest_window():
    calculate_crest_needs = arcana_crest_calculator()
    
    crest_window = tk.Toplevel()
    crest_window.title("🦧 Crest Calculator")
    crest_window.geometry("700x600")  
    
    input_frame = ttk.Frame(crest_window, padding="20")
    input_frame.pack(fill=tk.X)
    
    ttk.Label(input_frame, text="Current Link Stage (0-10):").grid(row=0, column=0, sticky="w", pady=5)
    current_stage_entry = ttk.Entry(input_frame, width=15)
    current_stage_entry.grid(row=0, column=1, padx=10, pady=5)
    
    ttk.Label(input_frame, text="Target Link Stage (1-10):").grid(row=1, column=0, sticky="w", pady=5)
    target_stage_entry = ttk.Entry(input_frame, width=15)
    target_stage_entry.grid(row=1, column=1, padx=10, pady=5)
    
    ttk.Label(input_frame, text="--- Current Inventory ---", font=('Arial', 10, 'bold')).grid(row=2, column=0, columnspan=2, pady=(15,5))
    
    ttk.Label(input_frame, text="Scorching Crests owned:").grid(row=3, column=0, sticky="w", pady=2)
    scorching_entry = ttk.Entry(input_frame, width=15)
    scorching_entry.grid(row=3, column=1, padx=10, pady=2)
    
    ttk.Label(input_frame, text="Ice-Scorched Crests owned:").grid(row=4, column=0, sticky="w", pady=2)
    ice_entry = ttk.Entry(input_frame, width=15)
    ice_entry.grid(row=4, column=1, padx=10, pady=2)
    
    ttk.Label(input_frame, text="Smoldering Threads owned:").grid(row=5, column=0, sticky="w", pady=2)
    smoldering_entry = ttk.Entry(input_frame, width=15)
    smoldering_entry.grid(row=5, column=1, padx=10, pady=2)
    
    ttk.Label(input_frame, text="Frostflame Threads owned:").grid(row=6, column=0, sticky="w", pady=2)
    frostflame_entry = ttk.Entry(input_frame, width=15)
    frostflame_entry.grid(row=6, column=1, padx=10, pady=2)
    
    calc_button = ttk.Button(input_frame, text="Calculate", 
                            command=lambda: calculate_crest_gui(current_stage_entry, target_stage_entry,
                                                               scorching_entry, ice_entry, smoldering_entry, 
                                                               frostflame_entry, result_table, calculate_crest_needs))
    calc_button.grid(row=7, column=0, columnspan=2, pady=15)
    
    result_frame = ttk.Frame(crest_window, padding="20")
    result_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(result_frame, text="Results:", font=('Arial', 12, 'bold')).pack(anchor="w")
    
    # table with column widths
    columns = ('Item', 'Still Need', 'Threads Required', 'Gold Cost')
    result_table = ttk.Treeview(result_frame, columns=columns, show='headings', height=12)
    
    # headers and widths
    result_table.heading('Item', text='Item')
    result_table.heading('Still Need', text='Still Need')
    result_table.heading('Threads Required', text='Threads Required') 
    result_table.heading('Gold Cost', text='Gold Cost')
    
    result_table.column('Item', width=240, anchor='w')  # Much wider for requirements
    result_table.column('Still Need', width=100, anchor='center')
    result_table.column('Threads Required', width=120, anchor='center')
    result_table.column('Gold Cost', width=150, anchor='e')
    
    result_table.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # scrollbars
    v_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_table.yview)
    v_scrollbar.pack(side="right", fill="y")
    result_table.configure(yscrollcommand=v_scrollbar.set)

def calculate_crest_gui(current_stage_entry, target_stage_entry, scorching_entry,
                       ice_entry, smoldering_entry, frostflame_entry, result_table, calculate_crest_needs):
    try:
        current_stage = int(current_stage_entry.get())
        target_stage = int(target_stage_entry.get())
        
        current_scorching = int(scorching_entry.get()) if scorching_entry.get().strip() else 0
        current_ice = int(ice_entry.get()) if ice_entry.get().strip() else 0
        current_smoldering = int(smoldering_entry.get()) if smoldering_entry.get().strip() else 0
        current_frostflame = int(frostflame_entry.get()) if frostflame_entry.get().strip() else 0
        
        result = calculate_crest_needs(current_stage, target_stage, current_scorching,
                                     current_ice, current_smoldering, current_frostflame)
        
        if isinstance(result, str):
            messagebox.showerror("Error", result)
            return
        
        # clear existing data
        for item in result_table.get_children():
            result_table.delete(item)
        
        #header info
        result_table.insert('', 'end', values=(
            f"📋 Stage {result['current_stage']} → {result['target_stage']}", '', '', ''
        ), tags=('header',))
        
        # requirements
        result_table.insert('', 'end', values=(
            f"🔥 Scorching Crests Required: {result['scorching_needed']}", '', '', ''
        ), tags=('info',))        
        if result['needs_ice']:
            result_table.insert('', 'end', values=(
                f"❄️ Ice-Scorched Crests Required: {result['ice_needed']}", '', '', ''
            ), tags=('info',))
        
        # separator
        result_table.insert('', 'end', values=('', '', '', ''), tags=('separator',))
        # main rows
        if result['scorching_to_get'] > 0 or result['scorching_gold_cost'] > 0:
            result_table.insert('', 'end', values=(
                '🔥 Scorching Crests',
                result['scorching_to_get'] if result['scorching_to_get'] > 0 else '✓ Complete',
                result['smoldering_to_buy'] if result['smoldering_to_buy'] > 0 else '—',
                f"{result['scorching_gold_cost']:,} gold" if result['scorching_gold_cost'] > 0 else '—'
            ))
        
        if result['needs_ice']:
            if result['ice_to_get'] > 0 or result['ice_gold_cost'] > 0:
                result_table.insert('', 'end', values=(
                    '❄️ Ice-Scorched Crests',
                    result['ice_to_get'] if result['ice_to_get'] > 0 else '✓ Complete',
                    result['frostflame_to_buy'] if result['frostflame_to_buy'] > 0 else '—',
                    f"{result['ice_gold_cost']:,} gold" if result['ice_gold_cost'] > 0 else '—'
                ))
        
        # total
        if result['total_gold_cost'] > 0:
            result_table.insert('', 'end', values=('', '', '', ''), tags=('separator',))
            result_table.insert('', 'end', values=(
                '💰💲 TOTAL COST', '', '', f"{result['total_gold_cost']:,} gold"
            ), tags=('total',))
        
        # row styles
        result_table.tag_configure('header', background='#e6f3ff', font=('Arial', 10, 'bold'))
        result_table.tag_configure('info', background='#f0f8ff', font=('Arial', 9, 'italic'))
        result_table.tag_configure('separator', background='#f5f5f5')
        result_table.tag_configure('total', background='#ffe6e6', font=('Arial', 10, 'bold'))
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# main GUI
def create_gui():
    root = tk.Tk()
    root.title("Arcana Calculators")
    root.geometry("400x300")
    
    # main frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # title
    title_label = ttk.Label(main_frame, text="Arcana Calculators", 
                           font=('Arial', 16, 'bold'))
    title_label.pack(pady=5)

    arcana_btn = ttk.Button(main_frame, text="🦍📈 Arcana Level Calculator 📈", 
                           command=lambda: open_calculator('arcana'))
    arcana_btn.pack(pady=10, fill=tk.X)

    crest_btn = ttk.Button(main_frame, text="🦧🔥 Crest Calculator ❄️", 
                          command=lambda: open_calculator('crest'))
    crest_btn.pack(pady=10, fill=tk.X)
    
    exit_btn = ttk.Button(main_frame, text="❌ Exit", command=root.quit)
    exit_btn.pack(pady=10)
    
    # subtitle
    subtitle_frame = ttk.Frame(main_frame)
    subtitle_frame.pack(pady=10)
    made_label = ttk.Label(subtitle_frame, text="made with ", 
                        font=('Arial', 9, 'italic'), anchor='center')
    made_label.pack(side='left')

    banana_label = ttk.Label(subtitle_frame, text="🍌", 
                            font=('Arial', 12), anchor='center')
    banana_label.pack(side='left', pady=(0,5))

    by_label = ttk.Label(subtitle_frame, text=" by ", 
                        font=('Arial', 9, 'italic'), anchor='center')
    by_label.pack(side='left')

    monkey_label = ttk.Label(subtitle_frame, text="🐒", 
                            font=('Arial', 12), anchor='center')
    monkey_label.pack(side='left', pady=(0, 5))
    
    def open_calculator(calc_type):
        if calc_type == 'arcana':
            open_arcana_window()
        else:
            open_crest_window()
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
