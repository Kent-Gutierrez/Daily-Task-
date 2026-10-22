from flask import Flask, render_template_string

app = Flask(__name__)

# Home page route — your full HTML/CSS/JS is embedded here
@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Task To-Do List</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        }

        :root {
            --bg-dark: #050508;
            --bg-card: #12121f;
            --bg-input: #1a1a2e;
            --accent: #00f0ff;
            --accent-alt: #a855f7;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --text-primary: #f0f0ff;
            --text-secondary: #9ca3af;
            --glow: 0 0 15px rgba(0, 240, 255, 0.35);
        }

        body {
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            padding-bottom: 85px;
        }

        header {
            background: linear-gradient(135deg, rgba(0,240,255,0.1), rgba(168,85,247,0.08));
            padding: 24px 20px 18px;
            border-bottom: 1px solid rgba(0, 240, 255, 0.15);
        }

        header h1 {
            font-size: 1.35rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--accent), var(--accent-alt));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stats-row {
            display: flex;
            gap: 10px;
            margin-top: 14px;
            flex-wrap: wrap;
        }

        .stat-card {
            flex: 1;
            min-width: 90px;
            background: var(--bg-card);
            border-radius: 12px;
            padding: 10px 12px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .stat-card .num {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--accent);
        }

        .stat-card .label {
            font-size: 0.7rem;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        .search-container {
            padding: 14px 20px;
        }

        #search {
            width: 100%;
            padding: 12px 16px;
            background: var(--bg-input);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 0.95rem;
            outline: none;
            transition: 0.25s;
        }

        #search:focus {
            border-color: var(--accent);
            box-shadow: var(--glow);
        }

        .tabs {
            display: flex;
            gap: 8px;
            padding: 0 20px 10px;
            overflow-x: auto;
        }

        .tab {
            padding: 8px 14px;
            background: var(--bg-card);
            border: none;
            color: var(--text-secondary);
            border-radius: 20px;
            font-size: 0.85rem;
            cursor: pointer;
            white-space: nowrap;
            transition: 0.25s;
        }

        .tab.active {
            background: linear-gradient(90deg, var(--accent), var(--accent-alt));
            color: #000;
            font-weight: 600;
        }

        .container {
            padding: 10px 20px;
        }

        .task-card {
            background: var(--bg-card);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.06);
            transition: 0.25s;
        }

        .task-card:hover {
            border-color: rgba(0, 240, 255, 0.25);
            transform: translateY(-2px);
        }

        .task-card.completed {
            opacity: 0.6;
            border-style: dashed;
        }

        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 8px;
        }

        .task-title {
            font-weight: 600;
            font-size: 0.98rem;
            text-decoration: none;
        }

        .task-card.completed .task-title {
            text-decoration: line-through;
            color: var(--text-secondary);
        }

        .priority-badge {
            font-size: 0.65rem;
            padding: 3px 8px;
            border-radius: 10px;
            font-weight: 700;
        }

        .priority-high { background: rgba(239,68,68,0.2); color: #fca5a5; }
        .priority-medium { background: rgba(245,158,11,0.2); color: #fcd34d; }
        .priority-low { background: rgba(16,185,129,0.2); color: #6ee7b7; }

        .task-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }

        .task-date {
            font-size: 0.78rem;
            color: var(--text-secondary);
        }

        .task-actions {
            display: flex;
            gap: 6px;
        }

        .action-btn {
            border: none;
            background: transparent;
            font-size: 1rem;
            cursor: pointer;
            padding: 4px 6px;
            border-radius: 6px;
            transition: 0.2s;
        }

        .action-btn:hover { background: rgba(255,255,255,0.08); }

        .fab {
            position: fixed;
            bottom: 100px;
            right: 20px;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), var(--accent-alt));
            border: none;
            font-size: 1.6rem;
            color: #000;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0, 240, 255, 0.4);
            z-index: 90;
        }

        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(10,10,18,0.9);
            backdrop-filter: blur(10px);
            display: flex;
            justify-content: space-around;
            padding: 10px 0 22px;
            border-top: 1px solid rgba(255,255,255,0.08);
            z-index: 100;
        }

        .nav-btn {
            display: flex;
            flex-direction: column;
            align-items: center;
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 0.7rem;
            gap: 3px;
            cursor: pointer;
        }

        .nav-btn.active { color: var(--accent); }

        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.75);
            display: none;
            align-items: flex-end;
            justify-content: center;
            z-index: 200;
            padding: 0;
        }

        .modal-overlay.show { display: flex; }

        .modal {
            background: var(--bg-card);
            width: 100%;
            max-width: 480px;
            border-radius: 20px 20px 0 0;
            padding: 24px 22px 30px;
            border: 1px solid rgba(0, 240, 255, 0.15);
        }

        .modal h2 {
            font-size: 1.15rem;
            margin-bottom: 18px;
            text-align: center;
        }

        .form-group {
            margin-bottom: 14px;
        }

        .form-group label {
            display: block;
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 5px;
        }

        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px 14px;
            background: var(--bg-input);
            border: 1px solid rgba(0, 240, 255, 0.15);
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 0.95rem;
            outline: none;
        }

        .form-group input:focus, .form-group select:focus {
            border-color: var(--accent);
            box-shadow: var(--glow);
        }

        .modal-buttons {
            display: flex;
            gap: 10px;
            margin-top: 8px;
        }

        .btn {
            flex: 1;
            padding: 13px;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.95rem;
        }

        .btn-cancel {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.15);
            color: var(--text-secondary);
        }

        .btn-save {
            background: linear-gradient(90deg, var(--accent), var(--accent-alt));
            color: #000;
        }

        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>

<header>
    <h1>✨ Daily Task To-Do List</h1>
    <div class="stats-row">
        <div class="stat-card">
            <div class="num" id="totalCount">0</div>
            <div class="label">Total</div>
        </div>
        <div class="stat-card">
            <div class="num" id="doneCount" style="color:var(--success)">0</div>
            <div class="label">Done</div>
        </div>
        <div class="stat-card">
            <div class="num" id="pendingCount" style="color:var(--warning)">0</div>
            <div class="label">Pending</div>
        </div>
    </div>
</header>

<div class="search-container">
    <input type="text" id="search" placeholder="🔍 Search tasks...">
</div>

<div class="tabs">
    <button class="tab active" data-filter="all">All</button>
    <button class="tab" data-filter="pending">Pending</button>
    <button class="tab" data-filter="completed">Completed</button>
    <button class="tab" data-filter="high">High</button>
    <button class="tab" data-filter="medium">Medium</button>
    <button class="tab" data-filter="low">Low</button>
</div>

<div class="container" id="taskList"></div>

<button class="fab" id="addBtn">+</button>

<nav class="bottom-nav">
    <button class="nav-btn active" data-view="home">
        <span>📋</span>Tasks
    </button>
    <button class="nav-btn" data-view="search">
        <span>🔍</span>Filter
    </button>
    <button class="nav-btn" data-view="export">
        <span>📥</span>Export
    </button>
</nav>

<div class="modal-overlay" id="modalOverlay">
    <div class="modal">
        <h2 id="modalTitle">➕ Add New Task</h2>
        <form id="taskForm">
            <input type="hidden" id="editId">
            
            <div class="form-group">
                <label>Task Title *</label>
                <input type="text" id="taskTitle" required placeholder="What needs to be done?">
            </div>
            
            <div class="form-group">
                <label>Description</label>
                <textarea id="taskDesc" rows="2" placeholder="More details..."></textarea>
            </div>
            
            <div class="form-group">
                <label>Due Date</label>
                <input type="date" id="taskDate">
            </div>
            
            <div class="form-group">
                <label>Priority</label>
                <select id="taskPriority">
                    <option value="high">🔴 High</option>
                    <option value="medium" selected>🟡 Medium</option>
                    <option value="low">🟢 Low</option>
                </select>
            </div>
            
            <div class="modal-buttons">
                <button type="button" class="btn btn-cancel" id="cancelBtn">Cancel</button>
                <button type="submit" class="btn btn-save">Save Task</button>
            </div>
        </form>
    </div>
</div>

<script>
let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
let currentFilter = 'all';

const taskList = document.getElementById('taskList');
const searchInput = document.getElementById('search');
const tabs = document.querySelectorAll('.tab');
const addBtn = document.getElementById('addBtn');
const modalOverlay = document.getElementById('modalOverlay');
const taskForm = document.getElementById('taskForm');
const cancelBtn = document.getElementById('cancelBtn');
const editId = document.getElementById('editId');

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
    renderTasks();
    updateStats();
}

function updateStats() {
    const total = tasks.length;
    const done = tasks.filter(t => t.completed).length;
    document.getElementById('totalCount').textContent = total;
    document.getElementById('doneCount').textContent = done;
    document.getElementById('pendingCount').textContent = total - done;
}

function renderTasks() {
    let filtered = [...tasks];
    
    const q = searchInput.value.toLowerCase().trim();
    if (q) {
        filtered = filtered.filter(t => 
            t.title.toLowerCase().includes(q) || 
            (t.desc && t.desc.toLowerCase().includes(q))
        );
    }
    
    if (currentFilter === 'pending') filtered = filtered.filter(t => !t.completed);
    if (currentFilter === 'completed') filtered = filtered.filter(t => t.completed);
    if (currentFilter === 'high') filtered = filtered.filter(t => t.priority === 'high');
    if (currentFilter === 'medium') filtered = filtered.filter(t => t.priority === 'medium');
    if (currentFilter === 'low') filtered = filtered.filter(t => t.priority === 'low');
    
    const prioOrder = { high: 0, medium: 1, low: 2 };
    filtered.sort((a, b) => prioOrder[a.priority] - prioOrder[b.priority]);
    
    if (!filtered.length) {
        taskList.innerHTML = `<div class="empty-state">
            <h3>📭 No tasks found</h3>
            <p>Tap + to add your first task!</p>
        </div>`;
        return;
    }
    
    taskList.innerHTML = filtered.map(task => `
        <div class="task-card ${task.completed ? 'completed' : ''}">
            <div class="task-header">
                <span class="task-title">${escapeHtml(task.title)}</span>
                <span class="priority-badge priority-${task.priority}">${task.priority.toUpperCase()}</span>
            </div>
            ${task.desc ? `<p style="font-size:0.8rem;color:var(--text-secondary);margin-top:6px;">${escapeHtml(task.desc)}</p>` : ''}
            <div class="task-meta">
                <span class="task-date">${task.dueDate || 'No due date'}</span>
                <div class="task-actions">
                    <button class="action-btn" title="Mark complete" onclick="toggleComplete('${task.id}')">${task.completed ? '↩️' : '✅'}</button>
                    <button class="action-btn" title="Edit" onclick="openEditModal('${task.id}')">✏️</button>
                    <button class="action-btn" title="Delete" onclick="deleteTask('${task.id}')">🗑️</button>
                </div>
            </div>
        </div>
    `).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function toggleComplete(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        saveTasks();
    }
}

function deleteTask(id) {
    if (confirm('Delete this task permanently?')) {
        tasks = tasks.filter(t => t.id !== id);
        saveTasks();
    }
}

function openEditModal(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        editId.value = id;
        document.getElementById('modalTitle').textContent = '✏️ Edit Task';
        document.getElementById('taskTitle').value = task.title;
        document.getElementById('taskDesc').value = task.desc || '';
        document.getElementById('taskDate').value = task.dueDate || '';
        document.getElementById('taskPriority').value = task.priority;
        modalOverlay.classList.add('show');
    }
}

function openAddModal() {
    editId.value = '';
    taskForm.reset();
    document.getElementById('modalTitle').textContent = '➕ Add New Task';
    modalOverlay.classList.add('show');
}

addBtn.addEventListener('click', openAddModal);
cancelBtn.addEventListener('click', () => modalOverlay.classList.remove('show'));

taskForm.addEventListener('submit', e => {
    e.preventDefault();
    const title = document.getElementById('taskTitle').value.trim();
    if (!title) return alert('Title is required!');
    
    const taskData = {
        title,
        desc: document.getElementById('taskDesc').value.trim(),
        dueDate: document.getElementById('taskDate').value,
        priority: document.getElementById('taskPriority').value
    };
    
    if (editId.value) {
        const task = tasks.find(t => t.id === editId.value);
        Object.assign(task, taskData);
    } else {
        tasks.unshift({
            id: Date.now().toString(),
            ...taskData,
            completed: false
        });
    }
    
    modalOverlay.classList.remove('show');
    saveTasks();
});

searchInput.addEventListener('input', renderTasks);

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentFilter = tab.dataset.filter;
        renderTasks();
    });
});

document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

document.querySelector('[data-view="export"]').addEventListener('click', () => {
    window.print();
});

renderTasks();
updateStats();
</script>

</body>
</html>
    """

if __name__ == '__main__':
    print("To-Do List Server Running!")
    print("Open in your browser: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)