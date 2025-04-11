let questions = [];
let currentIndex = 0;
const answers = {}

async function loadQuestions() {
  const response = await fetch("/data/questions.json");
  questions = await response.json();
  renderQuestion();
}
function handleEnter(event) {
  if (event.key === "Enter") {
    event.preventDefault(); 
    nextQuestion();         
  }
}

function renderQuestion() {
  const q = questions[currentIndex];
  const container = document.getElementById("questionContainer");

  let inputHtml = "";
  if (q.type === "dropdown") {
    inputHtml = `
      <select name="${q.name}" required
        class="w-full px-4 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-400 focus:outline-none">
        ${
          q.options.map(option =>
            typeof option === "object"
              ? `<option value="${option.value}">${option.label}</option>`
              : `<option value="${option}">${option}</option>`
          ).join("")
        }
      </select>`;
  } else if (q.type === "number") {
    inputHtml = `
      <input type="number" name="${q.name}" min="${q.min}" max="${q.max}" required
        class="w-full px-4 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-400 focus:outline-none" />`;
  }

  container.innerHTML = `
    <h2 class="text-xl font-semibold text-purple-800 mb-4">${q.label}</h2>
    ${inputHtml}`;

  document.getElementById("backBtn").disabled = currentIndex === 0;
  document.getElementById("nextBtn").innerText = currentIndex === questions.length - 1 ? "Submit" : "Next";
}

function showResult(prediction) {
    const quizForm = document.getElementById("quizForm");
    quizForm.innerHTML = `
      <div class="bg-purple-100 p-6 rounded-xl shadow-xl text-center">
        <h2 class="text-3xl font-bold text-purple-900 mb-4">Your Result</h2>
        <p class="text-xl text-purple-800">${prediction}</p>
      </div>
    `;
  }
  
  function getUserInputValue() {
    const input = document.querySelector("#questionContainer select, #questionContainer input");
    if (!input) return null;

    const value = input.value;
  
    if (input.type === "number") {
      const min = parseFloat(input.min);
      const max = parseFloat(input.max);
      const numValue = parseFloat(value);
  
      if (isNaN(numValue) || numValue < min || numValue > max) {
        alert(`Please enter a value between ${min} and ${max}`);
        return null;
      }
    }
  
    return input ? input.value : null;
  }
  function nextQuestion() {
    const inputValue = getUserInputValue();
    if (inputValue === null || inputValue === "") return;
  
    const currentQuestion = questions[currentIndex];
    let value = document.querySelector(`[name="${currentQuestion.name}"]`).value;
  
    if (currentQuestion.type === "number") {
      value = currentQuestion.float ? parseFloat(value) : parseInt(value);
    } else if (currentQuestion.type === "dropdown") {

      if (!isNaN(value) && value.trim() !== "") {
        value = value.includes('.') ? parseFloat(value) : parseInt(value);
      }
    }
  
    answers[currentQuestion.name] = value;
  
    if (currentIndex < questions.length - 1) {
      currentIndex++;
      renderQuestion();
    } else {
      fetch("https://depresso-z4g4.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(answers),
      })
        .then((res) => res.json())
        .then((data) => {
          showResult(data.prediction);
        })
        .catch((err) => console.error("Error sending data:", err));
    }
  }
  
  
  function prevQuestion() {
    const inputValue = getUserInputValue();
    if (inputValue !== null) {
      answers[questions[currentIndex].name] = inputValue;
    }
  
    if (currentIndex > 0) {
      currentIndex--;
      renderQuestion();
    }
  }
  
window.onload = loadQuestions;
