import streamlit as st
import pandas as pd
import datetime
import random

# Konfiguration der Seite
st.set_page_config(
    page_title="Task me if you can",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Basis-Styling für die App
st.markdown("""
<style>
    /* Allgemeines Styling */
    .stApp {
        font-family: 'Arial', sans-serif;
    }

    /* Karten-Design */
    .task-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid var(--border-color, #e0e0e0);
        background-color: var(--background-color, #ffffff);
        color: var(--text-color, #000000);
    }

    /* Fortschrittsbalken */
    .stProgress > div > div {
        height: 8px;
        border-radius: 4px;
    }

    /* Animation für Emojis */
    .floating-emoji {
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
</style>
""", unsafe_allow_html=True)

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


# Initialisierung Session State
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'deleted_tasks' not in st.session_state:
    st.session_state.deleted_tasks = []

def restore_task(task, source_list, index):
    """Stellt eine Aufgabe wieder her"""
    task['done'] = False
    st.session_state.tasks.append(task)
    source_list.pop(index)
    return task['title']

# Seitenwahl mit Icons
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Wähle eine Seite:", 
    ["📋 Aktive Aufgaben", "✅ Erledigte Aufgaben", "🗑️ Gelöschte Aufgaben", "📅 Kalender"])

if "📋 Aktive Aufgaben" in page:
    st.title("🎓 Task me if you can")
    
    # Motivationsspruch mit Animation
    col1, col2 = st.columns([4, 1])
    with col1:
        st.info(random.choice(MOTIVATION_QUOTES))
    with col2:
        st.markdown(f"""
            <div class='floating-emoji' style='font-size: 2rem; text-align: center;'>
                {random.choice(ANIMATION_EMOJIS)}
            </div>
        """, unsafe_allow_html=True)

    # Formular für neue Aufgaben
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
                <div class='task-card'>
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
    with st.expander("⏰ Erinnerungen", expanded=True):
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
        else:
            st.success("🎉 Keine überfälligen Aufgaben!")

elif "✅ Erledigte Aufgaben" in page:
    st.title("✅ Erledigte Aufgaben")
    
    erledigte_tasks = [task for task in st.session_state.tasks if task['done']]

    if not erledigte_tasks:
        st.info("🎯 Noch keine erledigten Aufgaben vorhanden.")
    else:
        for i, task in enumerate(erledigte_tasks):
            with st.container():
                st.markdown(f"""
                    <div class='task-card'>
                        <h3>{task['title']}</h3>
                        <p>Priorität: {task['priority']} | Fällig am: {task['due_date']}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(task['progress'])

                if st.button("↩️ Wiederherstellen", key=f"restore_{i}"):
                    restore_task(task, erledigte_tasks, i)
                    st.success(f"✅ Aufgabe '{task['title']}' wurde wiederhergestellt!")
                    st.rerun()

elif "🗑️ Gelöschte Aufgaben" in page:
    st.title("🗑️ Gelöschte Aufgaben")

    if not st.session_state.deleted_tasks:
        st.info("🗑️ Keine gelöschten Aufgaben vorhanden.")
    else:
        for i, task in enumerate(st.session_state.deleted_tasks):
            with st.container():
                st.markdown(f"""
                    <div class='task-card'>
                        <h3>{task['title']}</h3>
                        <p>Priorität: {task['priority']} | Fällig am: {task['due_date']}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(task['progress'])

                if st.button("↩️ Wiederherstellen", key=f"restore_deleted_{i}"):
                    restore_task(task, st.session_state.deleted_tasks, i)
                    st.success(f"✅ Aufgabe '{task['title']}' wurde wiederhergestellt!")
                    st.rerun()

else:  # Kalender
    st.title("📅 Aufgaben-Kalender")
    
    if not st.session_state.tasks:
        st.info("📅 Keine Aufgaben im Kalender vorhanden.")
    else:
        # Wochenansicht
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]

        st.subheader("📅 Diese Woche")
        cols = st.columns(7)
        
        # Tage der Woche
        for col, date in zip(cols, dates):
            with col:
                if date == today:
                    st.markdown(f"**{date.strftime('%a %d')}**")
                else:
                    st.write(date.strftime('%a %d'))

        # Aufgaben pro Tag
        for _ in range(3):  # Maximal 3 Aufgaben pro Tag
            cols = st.columns(7)
            for col, date in zip(cols, dates):
                with col:
                    day_tasks = [t for t in st.session_state.tasks if t['due_date'] == date]
                    if day_tasks:
                        task = day_tasks[0]
                        st.markdown(f"""
                            <div class='task-card' style='font-size: 0.8em;'>
                                {task['title'][:20]}{'...' if len(task['title']) > 20 else ''}
                                <br>{'✅' if task['done'] else '🕒'} {task['progress']}%
                            </div>
                        """, unsafe_allow_html=True)

        # Detailansicht
        st.subheader("📋 Alle Aufgaben")
        calendar_data = pd.DataFrame([
            {
                "📝 Aufgabe": task['title'],
                "📅 Fälligkeitsdatum": task['due_date'],
                "✅ Status": "Erledigt" if task['done'] else "Offen",
                "🎯 Priorität": task['priority'],
                "📊 Fortschritt": f"{task['progress']}%"
            }
            for task in st.session_state.tasks
        ]).sort_values("📅 Fälligkeitsdatum")

        st.dataframe(calendar_data, use_container_width=True)