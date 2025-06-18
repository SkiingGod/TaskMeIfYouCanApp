import streamlit as st
import pandas as pd
import datetime
import random

def restore_task(task, source_list, index):
    """Stellt eine Aufgabe wieder her"""
    task['done'] = False
    st.session_state.tasks.append(task)
    source_list.pop(index)
    return task['title']

# Konfiguration der Seite für bessere Responsivität
st.set_page_config(
    page_title="Task me if you can",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'Task me if you can - Your Personal Task Manager'
    }
)

# Animation Emojis für die Motivationssprüche
ANIMATION_EMOJIS = [
    "🏃‍♂️💨", "⭐️✨", "🌈🌟", "🎯💫", "💪🔥", "🚀✨", "🌞🌈", "🎉✨", "🦸‍♂️💫", "🎨💫",
    "🌱🌿", "🎸💫", "⚡️💫", "🎭✨", "🎪🌟", "🎡💫", "🎢✨", "🎨🌈", "🎬💫", "🎮✨"
]

# Beispielhafte motivierende Sprüche
MOTIVATION_QUOTES = [

    "Je früher du anfängst, desto eher kannst du dich wieder wie ein Couch-Potato fühlen. 🥔",
    "Du bist nur eine erledigte Aufgabe von einem besseren Tag entfernt.🌤️",
    "Diese Aufgabe macht sich nicht von alleine. Du bist hier nicht bei Disney.🧚‍♀️",
    "Mach dir keinen Stress. Chaos hat auch seinen Charme. 🧨",
    "Du hast wieder nichts geschafft? Stark. Eine echte Konstante im Leben. 👏",
    "Dieser Task? Ach, der fühlt sich bestimmt geschmeichelt, so lange ignoriert zu werden. 💅",
    "Guck mal, Motivation! … Oh nein, war nur ein Hirngespinst. 🫥",
    "Zeit für deine Lieblingsbeschäftigung: Dinge tun, auf die du keinen Bock hast. 🎉",
    "Erledige sie jetzt – bevor sie sich mit anderen Aufgaben zu einer Armee verbündet. 🧟‍♂️",
    "Mach weiter, oder ich fang an zu schreien. 😤",
    "Wenn du's heute nicht machst, macht’s morgen niemand. 🫠",
    "Aufgaben lösen sich nicht von selbst. Leider. 😬",
    "Los jetzt, die Deadline wartet nicht auf faule Ausreden. ⏰",
    "Deine To-Do-Liste lacht dich gerade aus. Zeig ihr, wer der Boss ist. 😎",
    "Das ist keine Aufgabe. Das ist ein Charaktertest. 💥",
    "Jede nicht erledigte Aufgabe macht eine Katze traurig. 😿",
    "Du bist nicht müde. Du bist unmotiviert. Ändern wir das! 🔥",
    "Willst du chillen oder deinen Abschluss? Beides geht nicht. 💀",
    "Ich sag’s dir ungern, aber... du musst das jetzt machen. Sofort. 🫵",
    "Tu’s jetzt, sonst kommt der Lern-Goblin um Mitternacht. 🧌",
    "Erinnerst du dich an Motivation? Nein? Dann fang an! 🫵",
    "Diese Aufgabe erledigt sich nicht durch Scrollen. 📱✖️",
    "Du hast mehr Zeit als Ausreden. Los jetzt. 😠",
    "Wenn du’s nicht machst, mach ich’s... aber schlecht. 🧟‍♂️",
    "Deadline? Klingt wie dein Schicksal. 🔪",
    "Du bist nicht zu müde. Dein innerer Schweinehund hat nur WLAN. 🐷📶",
    "Jeder Klick auf ‚Später‘ löscht ein Hirnzellchen. 🧠🔥",
    "Entweder du erledigst die Aufgabe – oder sie erledigt dich. ☠️",
    "Du kannst nicht alles auf einmal tun 🤯 – aber du kannst alles auf die To-Do-Liste 📝 schieben!",
    "Eine erledigte Aufgabe am Morgen 🌅 vertreibt Kummer und Sorgen 😌",
    "Deine To-Do-Liste 📋 hat Gefühle 🥲 – tu ihr den Gefallen und streich was durch.",
    "Jeder kleine Schritt 🚶 bringt dich näher ans Ziel 🎯.",
    "Du bist nicht überfordert – du bist einfach auf dem Weg zu Großem 🌟.",
    "Heute ist ein guter Tag, um was Großes zu starten 🚀!",
    "Du brauchst keinen Plan B. Du brauchst Arsch hoch für Plan A 🍑🔥.",
    "Dein To-Do schreit nicht – aber dein Chef bald schon 📢😬.",

]


# Initialisierung Session State mit Standardwerten
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'deleted_tasks' not in st.session_state:
    st.session_state.deleted_tasks = []
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Modern Apple-like Design
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Modern Apple-like Design System */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Base Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Light/Dark Mode Colors */
    :root {
        --background-color: #ffffff;
        --text-color: #1a1a1a;
        --secondary-bg: #f7f7f7;
        --accent-color: #007AFF;
        --error-color: #FF3B30;
        --success-color: #34C759;
        --border-color: #e0e0e0;
        --card-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
    }

    [data-theme="dark"] {
        --background-color: #1a1a1a;
        --text-color: #ffffff;
        --secondary-bg: #2c2c2c;
        --accent-color: #0A84FF;
        --error-color: #FF453A;
        --success-color: #30D158;
        --border-color: #3a3a3a;
        --card-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
    }

    /* Container Styles */
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 3rem;
        margin: 0 auto;
    }

    /* Task Card Container */
    .task-container {
        background: var(--background-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--card-shadow);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .task-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }

    /* Form Styles */
    .stForm {
        background: var(--secondary-bg);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
    }

    .stTextInput input, .stSelectbox select, .stDateInput input {
        border-radius: 10px;
        border: 1px solid var(--border-color);
        padding: 0.75rem;
        background: var(--background-color);
        color: var(--text-color);
        font-size: 1rem;
        transition: all 0.2s ease;
    }

    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.1);
    }

    /* Button Styles */
    .stButton > button {
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        background: var(--accent-color);
        color: white;
        border: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.2);
    }

    /* Progress Bar */
    .stProgress > div {
        height: 8px;
        border-radius: 4px;
        background: var(--secondary-bg);
    }

    .stProgress > div > div {
        background: var(--accent-color);
        border-radius: 4px;
    }

    /* Typography */
    h1 {
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        color: var(--text-color);
        letter-spacing: -0.02em;
    }

    h2, h3 {
        font-weight: 600;
        color: var(--text-color);
        letter-spacing: -0.01em;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: var(--secondary-bg);
        border-right: 1px solid var(--border-color);
        padding: 2rem 1rem;
    }

    /* Calendar View */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-color);
        background: var(--background-color);
    }

    .dataframe th {
        background: var(--secondary-bg);
        padding: 1rem;
        font-weight: 600;
    }

    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border-color);
    }

    /* Alerts and Messages */
    .stAlert {
        border-radius: 12px;
        border: none;
        padding: 1rem;
    }

    /* Animation for Emoji */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    .floating-emoji {
        animation: float 3s ease-in-out infinite;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }

        h1 {
            font-size: 2rem;
        }

        .stForm {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Seitenwahl mit verbesserten Icons
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Wähle eine Seite:", 
    ["📋 Aktive Aufgaben", "✅ Erledigte Aufgaben", "🗑️ Gelöschte Aufgaben", "📅 Kalender"])

# Container für den Hauptinhalt
main_container = st.container()

with main_container:
    if "📋 Aktive Aufgaben" in page:
        st.title("🎓 Task me if you can")
        
        # Motivationsspruch mit Animation in einem Container
        motivation_container = st.container()
        with motivation_container:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                    <div style='background: var(--secondary-bg); 
                             padding: 1rem; 
                             border-radius: 12px; 
                             margin-bottom: 1rem;'>
                        <h3>{random.choice(MOTIVATION_QUOTES)}</h3>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class='floating-emoji' style='font-size: 2rem; text-align: center;'>
                        {random.choice(ANIMATION_EMOJIS)}
                    </div>
                """, unsafe_allow_html=True)

        # Formular für neue Aufgaben in einem Container
        with st.expander("➕ Neue Aufgabe hinzufügen", expanded=False):
            with st.form("new_task_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    title = st.text_input("📝 Aufgabentitel")
                    priority = st.selectbox("🎯 Priorität", ["Hoch", "Mittel", "Niedrig"])
                with col2:
                    due_date = st.date_input("📅 Fälligkeitsdatum", datetime.date.today())
                    shared_with = st.text_input("👥 Teilen mit (optional)")
                
                progress = st.slider("📊 Fortschritt (%)", 0, 100, 0)
                submitted = st.form_submit_button("✨ Aufgabe hinzufügen")

                if submitted and title:
                    st.session_state.tasks.append({
                        "title": title,
                        "due_date": due_date,
                        "priority": priority,
                        "shared_with": shared_with,
                        "done": False,
                        "progress": progress
                    })
                    st.success("✅ Aufgabe erfolgreich hinzugefügt!")

        # Aktive Aufgaben
        st.header("📝 Deine Aufgaben")
        
        # Filtern und Sortieren
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("🔄 Sortieren nach", ["Fälligkeitsdatum", "Priorität", "Fortschritt"])
        with col2:
            filter_priority = st.multiselect("🔍 Nach Priorität filtern", ["Hoch", "Mittel", "Niedrig"])

        # Tasks verarbeiten
        tasks_to_display = [task for task in st.session_state.tasks if not task['done']]
        
        if sort_by == "Fälligkeitsdatum":
            tasks_to_display.sort(key=lambda x: x['due_date'])
        elif sort_by == "Priorität":
            priority_order = {"Hoch": 0, "Mittel": 1, "Niedrig": 2}
            tasks_to_display.sort(key=lambda x: priority_order[x['priority']])
        else:
            tasks_to_display.sort(key=lambda x: x['progress'], reverse=True)

        if filter_priority:
            tasks_to_display = [task for task in tasks_to_display if task['priority'] in filter_priority]

        if not tasks_to_display:
            st.info("🎉 Keine aktiven Aufgaben vorhanden!")
        
        for i, task in enumerate(tasks_to_display):
            with st.container():
                st.markdown(f"""
                    <div class='task-container'>
                        <h3>{task['title']}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
                with col1:
                    st.progress(task['progress'])
                    task['progress'] = st.slider("Fortschritt", 0, 100, task['progress'], key=f"progress_{i}")
                with col2:
                    task['done'] = st.checkbox("✓", value=task['done'], key=f"done_{i}")
                with col3:
                    if st.button("🗑️", key=f"delete_{i}"):
                        st.session_state.deleted_tasks.append(task)
                        st.session_state.tasks.remove(task)
                        st.rerun()
                with col4:
                    priority_color = {
                        "Hoch": "🔴",
                        "Mittel": "🟡",
                        "Niedrig": "🟢"
                    }
                    st.write(f"{priority_color[task['priority']]} {task['priority']}")

        # Erinnerungen
        st.header("⏰ Erinnerungen")
        today = datetime.date.today()
        overdue_tasks = [task for task in st.session_state.tasks 
                        if not task['done'] and task['due_date'] <= today]
        
        if overdue_tasks:
            for task in overdue_tasks:
                days_overdue = (today - task['due_date']).days
                if days_overdue > 0:
                    st.warning(f"⚠️ '{task['title']}' ist {days_overdue} Tage überfällig!")
                else:
                    st.info(f"📅 '{task['title']}' ist heute fällig!")

    # Seite: Erledigte Aufgaben
    elif page == "✅ Erledigte Aufgaben":
        st.title("✅ Erledigte Aufgaben")
        
        erledigte_tasks = [task for task in st.session_state.tasks if task['done']]

        if not erledigte_tasks:
            st.info("🎯 Noch keine erledigten Aufgaben vorhanden.")
        else:
            for i, task in enumerate(erledigte_tasks):
                with st.container():
                    st.markdown(f"""
                        <div class='task-container'>
                            <h3>{task['title']}</h3>
                            <p>Priorität: {task['priority']} | Fällig am: {task['due_date']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.progress(task['progress'])

                    if st.button("↩️ Wiederherstellen", key=f"restore_{i}"):
                        restored_title = restore_task(task, erledigte_tasks, i)
                        st.success(f"✅ Aufgabe '{restored_title}' wurde wiederhergestellt!")
                        st.rerun()

    # Seite: Gelöschte Aufgaben
    elif page == "🗑️ Gelöschte Aufgaben":
        st.title("🗑️ Gelöschte Aufgaben")

        if not st.session_state.deleted_tasks:
            st.info("🗑️ Keine gelöschten Aufgaben vorhanden.")
        else:
            for i, task in enumerate(st.session_state.deleted_tasks):
                with st.container():
                    st.markdown(f"""
                        <div class='task-container'>
                            <h3>{task['title']}</h3>
                            <p>Priorität: {task['priority']} | Fällig am: {task['due_date']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.progress(task['progress'])

                    if st.button("↩️ Wiederherstellen", key=f"restore_deleted_{i}"):
                        restored_title = restore_task(task, st.session_state.deleted_tasks, i)
                        st.success(f"✅ Aufgabe '{restored_title}' wurde wiederhergestellt!")
                        st.rerun()

    # Seite: Kalender
    elif page == "📅 Kalender":
        st.title("📅 Aufgaben-Kalender")

        if not st.session_state.tasks:
            st.info("📅 Keine Aufgaben im Kalender vorhanden.")
        else:
            # Kalenderansicht mit verbesserten Styles
            calendar_data = pd.DataFrame([
                {
                    "📝 Aufgabe": task['title'],
                    "📅 Fälligkeitsdatum": pd.to_datetime(task['due_date']),
                    "✅ Status": "Erledigt" if task['done'] else "Offen",
                    "🎯 Priorität": task['priority'],
                    "📊 Fortschritt": f"{task['progress']}%"
                }
                for task in st.session_state.tasks
            ]).sort_values("📅 Fälligkeitsdatum")

            # Füge Styling zum DataFrame hinzu
            def color_status(val):
                return 'background-color: #34C759; color: white' if val == "Erledigt" else 'background-color: #007AFF; color: white'

            def color_priority(val):
                colors = {
                    "Hoch": '#FF3B30',
                    "Mittel": '#FF9500',
                    "Niedrig": '#34C759'
                }
                return f'background-color: {colors[val]}; color: white'

            # Style das DataFrame
            styled_df = calendar_data.style\
                .applymap(color_status, subset=["✅ Status"])\
                .applymap(color_priority, subset=["🎯 Priorität"])\
                .set_properties(**{
                    'background-color': 'var(--background-color)',
                    'color': 'var(--text-color)',
                    'border-color': 'var(--border-color)'
                })

            st.dataframe(styled_df, use_container_width=True)

            # Statistiken
            st.subheader("📊 Aufgaben-Statistiken")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_tasks = len(st.session_state.tasks)
                completed_tasks = len([t for t in st.session_state.tasks if t['done']])
                completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                st.metric("Erledigungsquote", f"{completion_rate:.1f}%")
            
            with col2:
                high_priority = len([t for t in st.session_state.tasks if t['priority'] == "Hoch"])
                st.metric("Hochprioritäre Aufgaben", high_priority)
            
            with col3:
                avg_progress = sum(t['progress'] for t in st.session_state.tasks) / len(st.session_state.tasks) if st.session_state.tasks else 0
                st.metric("Durchschnittlicher Fortschritt", f"{avg_progress:.1f}%")