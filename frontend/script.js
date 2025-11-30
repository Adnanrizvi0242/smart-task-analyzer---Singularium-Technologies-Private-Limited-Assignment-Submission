let tasks = [];
let chart = null;

// DARK MODE
document.getElementById("themeToggle").addEventListener("click", () => {
    document.body.classList.toggle("dark");
});

// ADD TASK
document.getElementById("addTaskBtn").addEventListener("click", () => {
    const t = {
        title: document.getElementById("title").value,
        due_date: document.getElementById("due_date").value,
        estimated_hours: parseFloat(document.getElementById("estimated_hours").value),
        importance: parseInt(document.getElementById("importance").value),
        dependencies: document.getElementById("dependencies").value
            ? document.getElementById("dependencies").value.split(",").map(Number)
            : []
    };

    tasks.push(t);
    alert("Task added!");
});

// ANALYZE TASKS
document.getElementById("analyzeBtn").addEventListener("click", async () => {
    let payload = tasks;

    const loader = document.getElementById("loader");
    loader.classList.remove("hidden");

    const strategy = document.getElementById("strategy").value;

    const response = await fetch(
        "http://127.0.0.1:8000/api/tasks/analyze/?mode=" + strategy,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        }
    );

    loader.classList.add("hidden");
    const data = await response.json();
    renderResults(data);
    drawChart(data);
});

// RENDER RESULTS
function renderResults(data) {
    const box = document.getElementById("results");
    box.innerHTML = "";

    data.forEach(t => {
        let level = t.score >= 30 ? "high" : t.score >= 25 ? "medium" : "low";

        box.innerHTML += `
            <div class="task-card ${level}" draggable="true">
                <h3>${t.title}</h3>
                <p><strong>Score:</strong> ${t.score.toFixed(2)}</p>
                <p>${t.explanation}</p>
            </div>
        `;
    });

    enableDragDrop();
}

// DRAG & DROP
function enableDragDrop() {
    const cards = document.querySelectorAll(".task-card");
    cards.forEach(card => {
        card.addEventListener("dragstart", e => {
            e.target.classList.add("dragging");
        });
        card.addEventListener("dragend", e => {
            e.target.classList.remove("dragging");
        });
    });

    const list = document.getElementById("results");
    list.addEventListener("dragover", e => {
        e.preventDefault();
        const dragging = document.querySelector(".dragging");
        list.appendChild(dragging);
    });
}

// CHART
function drawChart(data) {
    const labels = data.map(t => t.title);
    const scores = data.map(t => t.score);

    if (chart) chart.destroy();

    chart = new Chart(document.getElementById("priorityChart"), {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Task Priority Score",
                data: scores,
                backgroundColor: ["#e63946","#ffca3a","#2ecc71","#48cae4"],
            }]
        }
    });
}

// EXPORT PDF
document.getElementById("exportPDF").addEventListener("click", () => {
    const content = document.body.innerHTML;
    const win = window.open("", "", "width=900,height=900");
    win.document.write(content);
    win.print();
});
