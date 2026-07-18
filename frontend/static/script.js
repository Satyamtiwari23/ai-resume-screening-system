console.log("SCRIPT VERSION 1.0");
const fileInput = document.getElementById("resume");
const circle = document.querySelector(".circle");
const jobRequirements = document.getElementById("jobRequirements");

if (jobRequirements) {
    jobRequirements.style.display = "block";
}
// MODE SWITCH
let currentMode = "hr";
let viewingCandidate = false;
let uploadedFiles = [];

function clearUploadedFiles() {

    uploadedFiles = [];
    fileInput.value = "";

    document.getElementById("selectedFile").innerHTML =
        "No Resume Selected";

    // Reset Timeline
    document.querySelectorAll(".timeline-step").forEach(step => {

        step.classList.remove("done");

    });

    document.getElementById("statusText").innerHTML = "";

    document.getElementById("statusText").innerHTML = "";

}

const uploadHeading = document.getElementById("uploadHeading");
const uploadButton = document.querySelector(".drop-area button");
const analyzeBtn = document.querySelector(".analyzeBtn");
const hrDashboard = document.getElementById("hrDashboard");

const analysisCard = document.getElementById("candidateModal");

const tableBody = document.getElementById("candidateTableBody");
function animateScore(score) {

    clearInterval(window.scoreTimer);

    let current = 0;

    document.getElementById("atsScore").innerHTML = "0%";

    circle.style.background =
        "conic-gradient(#2563eb 0deg,#dbeafe 0deg)";

    window.scoreTimer = setInterval(() => {

        current++;

        document.getElementById("atsScore").innerHTML = current + "%";

        circle.style.background =
            `conic-gradient(#2563eb ${current * 3.6}deg,#dbeafe ${current * 3.6}deg)`;

        if (current >= score) {

            clearInterval(window.scoreTimer);

        }

    }, 18);

}

fileInput.addEventListener("change", () => {

    const newFiles = Array.from(fileInput.files);

    if (currentMode === "student") {

        uploadedFiles = newFiles.slice(0, 1);

    } else {

        newFiles.forEach(file => {

            if (!uploadedFiles.some(f =>
                f.name === file.name &&
                f.size === file.size
            )) {
                uploadedFiles.push(file);
            }
            document.getElementById("studentSidebar").classList.remove("hidden");
        });

    }

    document.getElementById("uploadTitle").innerHTML = "Resume Selected";
    document.getElementById("uploadSubtitle").innerHTML = "Ready to Analyze";

    if (currentMode === "student") {

        document.getElementById("selectedFile").innerHTML =
            "📄 " + uploadedFiles[0].name;

    } else {

        document.getElementById("selectedFile").innerHTML =
            `📂 ${uploadedFiles.length} resumes selected`;

    }

    // Reset input so selecting the same file again triggers change
    fileInput.value = "";

});

async function uploadResume() {

    if (uploadedFiles.length === 0) {
        alert("Please select resume(s)");
        return;
    }

    const analyzeBtn = document.querySelector(".analyzeBtn");
    const loader = document.getElementById("loader");

    loader.classList.remove("hidden");

    const status = document.getElementById("statusText");

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = "⏳ Analyzing...";
    status.innerHTML = "📤 Uploading Resume...";
    document.getElementById("step1").classList.add("done");

    const formData = new FormData();

    console.log("================================");
    console.log("Current Mode:", currentMode);
    console.log("Uploaded Files:", uploadedFiles.length);

    uploadedFiles.forEach((file, index) => {
        console.log(index + 1, file.name);
    });

    console.log("================================");

    for (const file of uploadedFiles) {
        console.log("Appending:", file.name);
        formData.append("resumes", file);
    }
    formData.append(
        "requiredSkills",
        document.getElementById("requiredSkills").value
    );

    formData.append(
        "department",
        document.getElementById("department").value
    );

    formData.append(
        "jobRole",
        document.getElementById("jobRole").value
    );

    formData.append(
        "experience",
        document.getElementById("experience").value
    );

    formData.append(
        "education",
        document.getElementById("education").value
    );

    try {
        console.log("Sending request...");
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        status.innerHTML = "📄 Reading PDF...";
        document.getElementById("step2").classList.add("done");

        const data = await response.json();
        const toast = document.getElementById("toast");

        toast.classList.remove("hidden");

        setTimeout(() => {

            toast.classList.add("hidden");

        }, 2500);
        status.innerHTML = "🧠 Extracting Information...";
        document.getElementById("step3").classList.add("done");

        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = currentMode === "hr" ? "Analyze Candidates" : "Analyze Resume";


        const resultDiv = document.getElementById("results");

        resultDiv.innerHTML = "";

        // ======================
        // HR MODE
        // ======================

        document.getElementById("step4").classList.add("done");
        document.getElementById("step5").classList.add("done");
        document.getElementById("step6").classList.add("done");
        if (data.candidates) {

            hrDashboard.classList.remove("hidden");
            analysisCard.classList.add("hidden");
            document.getElementById("downloadBtn").classList.add("hidden");
            document.getElementById("exportCSVBtn").classList.remove("hidden");

            tableBody.innerHTML = "";

            data.candidates.forEach((candidate, index) => {

                tableBody.innerHTML += `

        <tr>

            <td>${index + 1}</td>

            <td>${candidate.candidate.name}</td>

            <td>${candidate.score}%</td>

            <td>${candidate.predictedRole}</td>

            <td>${candidate.recommendation}</td>

            <td>

                <button

                    class="viewBtn"

                    onclick="showCandidate(${index})"

                >

                    View

                </button>

            </td>

        </tr>

        `;

            });

            window.hrCandidates = data.candidates;

            document.getElementById("totalCandidates").innerHTML =
                data.candidates.length;

            const avg =
                Math.round(
                    data.candidates.reduce((a, c) => a + c.score, 0)
                    / data.candidates.length
                );

            document.getElementById("averageATS").innerHTML =
                avg + "%";

            document.getElementById("topCandidate").innerHTML =
                data.candidates[0].candidate.name;

            document.getElementById("recommendedCount").innerHTML =
                data.candidates.filter(c => c.score >= 80).length;

            document.getElementById("topCandidateCard").innerHTML = `

            <div class="top-profile">
            
                <h2>${data.candidates[0].candidate.name}</h2>
            
                <div class="top-stat">
                    <span>ATS Score</span>
                    <strong>${data.candidates[0].score}%</strong>
                </div>
            
                <div class="top-stat">
                    <span>Role</span>
                    <strong>${data.candidates[0].predictedRole}</strong>
                </div>
            
                <div class="top-stat">
                    <span>Recommendation</span>
                    <strong>${data.candidates[0].recommendation}</strong>
                </div>


                <button
                    class="viewBtn"
                    onclick="showCandidate(0)"
                    style="margin-top:20px;width:100%;">
                    View Profile
                </button>
            
            </div>
            
            `;

            document.getElementById("recentAnalysis").innerHTML =
                `
            ${new Date().toLocaleString()}<br>

            ${data.candidates.length} candidates analyzed.
            `;

            loader.classList.add("hidden");

            status.innerHTML = "";

            return;

        }
        if (data.candidate) {
            renderCandidate(data);
        }
        else {

            resultDiv.innerHTML = `

        <div class="resume-card">

            <h3>No Resume Data Received</h3>

        </div>

    `;

        }
        document.getElementById("step4").classList.add("done");

        document.getElementById("step5").classList.add("done");

        document.getElementById("step6").classList.add("done");
        status.innerHTML = "✅ Analysis Complete";

        setTimeout(() => {

            loader.classList.add("hidden");

        }, 1000);

    } catch (error) {

        loader.classList.add("hidden");

        analyzeBtn.disabled = false;

        analyzeBtn.innerHTML = "Analyze Resume";

        console.error(error);

        status.innerHTML = "❌ Analysis Failed";

    }

}

function renderCandidate(data) {
    analysisCard.style.display = "block";
    const backBtn = document.getElementById("backDashboard");

    if (currentMode === "student") {
        backBtn.style.display = "none";
    } else {
        backBtn.style.display = "inline-block";
    }
    hrDashboard.classList.add("hidden");

    window.scrollTo({
        top: analysisCard.offsetTop - 20,
        behavior: "smooth"
    });

    document.getElementById("candidateName").innerHTML =
        data.candidate?.name || "Not Found";

    document.getElementById("candidateEmail").innerHTML =
        data.candidate?.email || "Not Found";

    document.getElementById("candidatePhone").innerHTML =
        data.candidate?.phone || "Not Found";

    document.getElementById("candidateExperience").innerHTML =
        data.candidate?.experience || "Not Found";

    document.getElementById("candidateEducation").innerHTML =
        data.candidate?.education || "Not Found";

    document.getElementById("resumeFile").innerHTML =
        data.candidate?.resume || "Not Found";

    document.getElementById("predictedRole").innerHTML =
        data.predictedRole || "Not Available";

    let summary = data.summary || "";

    if (Array.isArray(summary)) {
        summary = summary.join("\n");
    }

    summary = summary

        .replace(
            /👤 Overview/g,
            "<div class='summary-title overview'><i class='fa-solid fa-user'></i> Overview</div>"
        )

        .replace(
            /⭐ Final Verdict/g,
            "<div class='summary-title verdict'><i class='fa-solid fa-star'></i> Final Verdict</div>"
        )

        .replace(/\n/g, "<br>");

    document.getElementById("resumeSummary").innerHTML = summary;

    animateScore(data.score || 0);

    const breakdown = data.atsBreakdown || {};

    const sections = [

        ["skills", "skill"],

        ["experience", "experience"],

        ["education", "education"],

        ["projects", "project"],

        ["resume_quality", "quality"],

        ["certifications", "certificate"]

    ];

    sections.forEach(([key, id]) => {

        const value = breakdown[key] || 0;

        document.getElementById(id + "Score").innerHTML = value + "%";

        document.getElementById(id + "Bar").style.width = value + "%";

    });
    const strengths = document.getElementById("strengths");
    strengths.innerHTML = "";

    const weaknesses = document.getElementById("weaknesses");
    weaknesses.innerHTML = "";

    (data.weaknesses || []).forEach(item => {
        weaknesses.innerHTML += `<li>${item}</li>`;
    });

    (data.strengths || []).forEach(item => {
        strengths.innerHTML += `<li>${item}</li>`;
    });


    const feedbackCards = document.querySelectorAll(".feedback-card");

    if (currentMode === "hr") {

        feedbackCards[2].style.display = "none"; // Suggestions

        // Hiring Verdict
        feedbackCards[3].style.display = "";

        feedbackCards[4].style.display = "none"; // Interview Questions

    }
    else {

        feedbackCards[2].style.display = "";
        feedbackCards[3].style.display = "";

        feedbackCards[4].style.display = "";

    }
    const suggestions = document.getElementById("suggestions");
    suggestions.innerHTML = "";

    const hiring = data.hiring || {};
    document.getElementById("hiringConfidence").innerHTML =
        (hiring.confidence || 0) + "%";

    document.getElementById("hiringRisk").innerHTML =
        hiring.risk || "-";

    document.getElementById("hiringNotes").innerHTML =
        hiring.notes || "-";

    document.getElementById("hiringStatus").innerHTML =
        `${hiring.icon || ""} ${hiring.status || "-"}`;

    document.getElementById("hiringDecision").innerHTML =
        hiring.decision || "-";

    const hiringReasons =
        document.getElementById("hiringReasons");

    hiringReasons.innerHTML = "";

    (hiring.reason || []).forEach(reason => {

        hiringReasons.innerHTML +=
            `<li>${reason}</li>`;

    });

    const questions = document.getElementById("interviewQuestions");
    questions.innerHTML = "";

    (data.interviewQuestions || []).forEach(item => {
        questions.innerHTML += `<li>${item}</li>`;
    });

    (data.suggestions || []).forEach(item => {
        suggestions.innerHTML += `<li>${item}</li>`;
    });

    document.getElementById("recommendation").innerHTML =
        data.recommendation || "Not Available";

    const matched = document.getElementById("matchedSkills");
    matched.innerHTML = "";

    data.matchedSkills.forEach(skill => {

        matched.innerHTML +=

            `<span class="skill">${skill}</span>`;

    });

    const missing = document.getElementById("missingSkills");

    missing.innerHTML = "";

    data.missingSkills.forEach(skill => {

        missing.innerHTML +=

            `<span class="skill missing">${skill}</span>`;

    });
}
// Drag and Drop Feature

const dropArea = document.getElementById("dropArea");

dropArea.addEventListener("dragover", (e) => {

    e.preventDefault();

    dropArea.classList.add("dragover");

    document.getElementById("uploadTitle").innerHTML =
        "Drop Resume Here";

});

dropArea.addEventListener("dragleave", () => {

    dropArea.classList.remove("dragover");

    document.getElementById("uploadTitle").innerHTML =
        "Drag & Drop Resume Here";

});

dropArea.addEventListener("drop", (e) => {

    e.preventDefault();

    dropArea.classList.remove("dragover");

    const files = Array.from(e.dataTransfer.files);

    if (currentMode === "student") {

        uploadedFiles = [files[0]];

        document.getElementById("selectedFile").innerHTML =
            "📄 " + files[0].name;

    } else {

        files.forEach(file => {

            if (!uploadedFiles.some(f =>
                f.name === file.name &&
                f.size === file.size
            )) {
                uploadedFiles.push(file);
            }

        });

        document.getElementById("selectedFile").innerHTML =
            `📂 ${uploadedFiles.length} resumes selected`;

    }

});


// Theme

const themeBtn = document.getElementById("themeBtn");

if (localStorage.getItem("theme") == "dark") {

    document.body.classList.add("dark");

    themeBtn.innerHTML = "☀️";

}

themeBtn.addEventListener("click", () => {

    document.body.classList.toggle("dark");

    if (document.body.classList.contains("dark")) {

        themeBtn.innerHTML = "☀️";

        localStorage.setItem("theme", "dark");

    }

    else {

        themeBtn.innerHTML = "🌙";

        localStorage.setItem("theme", "light");

    }

});

const menuBtn = document.getElementById("menuBtn");

menuBtn.addEventListener("click", () => {

    const sidebar = document.querySelector(".sidebar");

    if (sidebar) {

        sidebar.classList.toggle("show");

    }

});



const settingsBtn = document.getElementById("settingsBtn");
const settingsMenu = document.getElementById("settingsMenu");

if (settingsBtn) {
    settingsBtn.onclick = () => {
        settingsMenu.classList.toggle("show");
    };
}

document.getElementById("toggleTheme").onclick = () => {

    themeBtn.click();

};

document.getElementById("resetAnalysis").onclick = () => {

    location.reload();

};

document.getElementById("aboutProject").onclick = () => {

    alert(
        `AI Resume Screening System
Version 1.0
Developed using HTML CSS JS Flask`
    );

};

function switchStudentMode() {

    currentMode = "student";

    updateSidebar();

    document.getElementById("downloadBtn").classList.remove("hidden");
    document.getElementById("exportCSVBtn").classList.add("hidden");

    uploadHeading.innerHTML = "Upload Resume";

    uploadButton.innerHTML = "📄 Choose Resume";

    analyzeBtn.innerHTML = "Analyze Resume";

    fileInput.removeAttribute("multiple");

    jobRequirements.style.display = "none";

    analysisCard.style.display = "block";

    hrDashboard.classList.add("hidden");

    clearUploadedFiles();

}

function switchHRMode() {

    currentMode = "hr";

    updateSidebar();

    document.getElementById("downloadBtn").classList.add("hidden");
    document.getElementById("exportCSVBtn").classList.remove("hidden");

    uploadHeading.innerHTML = "Upload Resumes";

    uploadButton.innerHTML = "📂 Choose Resumes";

    analyzeBtn.innerHTML = "Analyze Candidates";

    fileInput.setAttribute("multiple", true);

    jobRequirements.style.display = "block";

    analysisCard.style.display = "none";

    hrDashboard.classList.add("hidden");

    clearUploadedFiles();

}

function updateSidebar() {
    console.log("updateSidebar called");
    const mode = document.getElementById("sidebarMode");
    console.log("sidebar inserted");
    mode.innerHTML = `
    <div class="sidebar">

        <div class="brand">
            <i class="fa-solid fa-microchip"></i>
            <span>AI Resume ATS</span>
        </div>

        <div class="sidebar-mode">

            <div class="mode-title">
                ${currentMode === "student" ? "🎓 Student Mode" : "👔 HR Mode"}
            </div>

            <button
                id="modeSwitch"
                class="sidebar-switch">

                ${
                    currentMode === "student"
                    ? "👔 Switch to HR"
                    : "🎓 Switch to Student"
                }

            </button>

        </div>

        <ul id="sidebarMenu"></ul>

    </div>

    `;

    const menu = document.getElementById("sidebarMenu");

    if (currentMode === "student") {

        menu.innerHTML = `

<li class="active">
<i class="fa-solid fa-house"></i>
Dashboard
</li>

<li onclick="document.getElementById('resume').click()">
<i class="fa-solid fa-file-arrow-up"></i>
Upload Resume
</li>

<li onclick="document.getElementById('candidateModal').scrollIntoView({behavior:'smooth'})">
<i class="fa-solid fa-user"></i>
Candidate Analysis
</li>

<li onclick="document.getElementById('downloadBtn').click()">
<i class="fa-solid fa-download"></i>
Download Report
</li>

<hr>

<li onclick="location.reload()">
<i class="fa-solid fa-rotate-right"></i>
Reset
</li>

<li onclick="document.getElementById('settingsMenu').classList.toggle('show')">
<i class="fa-solid fa-gear"></i>
Settings
</li>

`;

    }

    else {

        menu.innerHTML = `

<li class="active">
<i class="fa-solid fa-house"></i>
Dashboard
</li>

<li onclick="document.getElementById('resume').click()">
<i class="fa-solid fa-folder-open"></i>
Upload Resumes
</li>

<li onclick="document.getElementById('hrDashboard').scrollIntoView({behavior:'smooth'})">
<i class="fa-solid fa-chart-line"></i>
Recruiter Dashboard
</li>

<li onclick="document.getElementById('exportCSVBtn').click()">
<i class="fa-solid fa-file-excel"></i>
Export Excel
</li>

<hr>

<li onclick="location.reload()">
<i class="fa-solid fa-rotate-right"></i>
Reset
</li>

<li onclick="document.getElementById('settingsMenu').classList.toggle('show')">
<i class="fa-solid fa-gear"></i>
Settings
</li>

`;

    }

    document.getElementById("modeSwitch").onclick = () => {

        if (currentMode === "student") {

            switchHRMode();

        } else {

            switchStudentMode();

        }

    };

}




function showCandidate(index) {

    const data = window.hrCandidates[index];
    viewingCandidate = true;
    hrDashboard.classList.add("hidden");

    analysisCard.style.display = "block";
    document.getElementById("downloadBtn").classList.remove("hidden");
    document.getElementById("exportCSVBtn").classList.add("hidden");

    renderCandidate(data);

    window.scrollTo({

        top: analysisCard.offsetTop - 20,

        behavior: "smooth"

    });

}

document.getElementById("backDashboard").onclick = () => {
    viewingCandidate = false;
    analysisCard.style.display = "none";

    hrDashboard.classList.remove("hidden");

    document.getElementById("downloadBtn").classList.add("hidden");
    document.getElementById("exportCSVBtn").classList.remove("hidden");

    window.scrollTo({
        top: hrDashboard.offsetTop - 20,
        behavior: "smooth"
    });

};


// =========================
// DOWNLOAD ATS REPORT
// =========================

document.getElementById("downloadBtn").addEventListener("click", () => {

    // Student Mode
    if (currentMode === "student") {

        downloadCandidateReport();
        return;
    }

    // HR Mode -> Individual Candidate
    if (viewingCandidate) {

        downloadCandidateReport();
        return;
    }

    // HR Dashboard
    downloadHRReport();

});

function downloadCandidateReport() {

    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    const blue = [37, 99, 235];
    const dark = [40, 40, 40];
    const green = [22, 163, 74];
    const red = [220, 38, 38];

    const PAGE_HEIGHT = doc.internal.pageSize.height;

    function checkPage(space = 35) {

        if (y + space > PAGE_HEIGHT - 20) {

            doc.addPage();

            y = 20;

            doc.setTextColor(...dark);

        }

    }

    //=========================
    // HEADER
    //=========================

    doc.setFillColor(...blue);
    doc.rect(0, 0, 210, 22, "F");

    doc.setFontSize(18);
    doc.setTextColor(255, 255, 255);
    doc.text("AI Resume Screening System", 14, 14);

    doc.setFontSize(12);
    doc.text("ATS REPORT", 165, 14);

    let y = 35;

    doc.setTextColor(...dark);

    doc.setFontSize(16);
    doc.text("Candidate Profile", 14, y);

    y += 8;

    doc.autoTable({

        startY: y,

        theme: "grid",

        styles: {
            fontSize: 10
        },

        head: [["Field", "Value"]],

        body: [

            ["Name", document.getElementById("candidateName").innerText],

            ["Email", document.getElementById("candidateEmail").innerText],

            ["Phone", document.getElementById("candidatePhone").innerText],

            ["Education", document.getElementById("candidateEducation").innerText],

            ["Experience", document.getElementById("candidateExperience").innerText],

            ["Predicted Role", document.getElementById("predictedRole").innerText]

        ]

    });

    y = doc.lastAutoTable.finalY + 12;

    //=========================
    // ATS SCORE
    //=========================

    doc.setFontSize(16);

    doc.text("ATS Evaluation", 14, y);

    y += 12;

    doc.setFillColor(240, 245, 255);

    doc.roundedRect(14, y - 6, 180, 16, 3, 3, "F");

    doc.setFontSize(13);

    doc.text("ATS Score", 20, y + 4);

    doc.setTextColor(...blue);

    doc.setFontSize(18);

    doc.text(document.getElementById("atsScore").innerText, 165, y + 4);

    y += 24;

    //=========================
    // Recommendation
    //=========================

    doc.setTextColor(...dark);

    doc.setFontSize(15);

    doc.text("Recommendation", 14, y);

    y += 8;

    doc.setTextColor(...green);

    doc.setFontSize(14);

    doc.text(document.getElementById("recommendation").innerText, 18, y);

    y += 15;


    //=========================
    // ATS BREAKDOWN
    //=========================

    doc.setTextColor(...dark);
    doc.setFontSize(15);
    doc.text("ATS Breakdown", 14, y);

    y += 8;

    doc.autoTable({
        startY: y,
        head: [["Criteria", "Score"]],
        body: [
            ["Skills", document.getElementById("skillScore").innerText],
            ["Experience", document.getElementById("experienceScore").innerText],
            ["Education", document.getElementById("educationScore").innerText],
            ["Projects", document.getElementById("projectScore").innerText],
            ["Resume Quality", document.getElementById("qualityScore").innerText],
            ["Certificates", document.getElementById("certificateScore").innerText]
        ],
        theme: "striped"
    });

    y = doc.lastAutoTable.finalY + 10;

    //=========================
    // Hiring Verdict
    //=========================

    doc.setTextColor(...dark);

    doc.setFontSize(15);

    doc.text("AI Hiring Verdict", 14, y);

    y += 10;

    doc.autoTable({

        startY: y,

        theme: "plain",

        body: [

            [
                "Status",
                document.getElementById("hiringStatus")
                    .innerText
                    .replace(/[^\x00-\x7F]/g, "")
                    .trim()
            ],

            ["Confidence", document.getElementById("hiringConfidence").innerText],

            ["Risk Level", document.getElementById("hiringRisk").innerText],

            ["Decision", document.getElementById("hiringDecision").innerText],

            ["Recruiter Notes", document.getElementById("hiringNotes").innerText]

        ]

    });

    y = doc.lastAutoTable.finalY + 10;

    doc.setFontSize(13);

    doc.text("Reasons", 14, y);

    y += 8;

    const reasons = [];

    document.querySelectorAll("#hiringReasons li").forEach(li => {

        reasons.push(["• " + li.innerText]);

    });

    doc.autoTable({

        startY: y,

        body: reasons,

        theme: "plain"

    });

    y = doc.lastAutoTable.finalY + 10;

    //=========================
    // Matched Skills
    //=========================

    doc.setFontSize(15);

    doc.text("Matched Skills", 14, y);

    y += 8;

    doc.setTextColor(...dark);

    doc.setFontSize(11);

    const matchedSkills = Array.from(
        document.querySelectorAll("#matchedSkills .skill")
    ).map(e => e.innerText).join(", ");

    doc.text(
        matchedSkills || "None",
        18,
        y,
        { maxWidth: 170 }
    );

    y += 20;

    //=========================
    // Missing Skills
    //=========================

    doc.setTextColor(...dark);

    doc.setFontSize(15);

    doc.text("Missing Skills", 14, y);

    y += 8;

    doc.setTextColor(...dark);

    doc.setFontSize(11);

    doc.text(

        Array.from(
            document.querySelectorAll("#missingSkills .skill")
        ).map(e => e.innerText).join(", "),

        18,

        y,

        { maxWidth: 170 }

    );

    y += 20;



    doc.setTextColor(...dark);
    doc.setFontSize(15);
    doc.text("Strengths", 14, y);

    y += 8;

    const strengths = [];

    document.querySelectorAll("#strengths li").forEach(li => {
        strengths.push(["✓ " + li.innerText]);
    });

    doc.autoTable({
        startY: y,
        body: strengths,
        theme: "plain"
    });

    y = doc.lastAutoTable.finalY + 10;


    //=========================
    // Weaknesses
    //=========================
    checkPage(45);
    doc.setFontSize(15);
    doc.text("Weaknesses", 14, y);

    y += 8;

    const weaknesses = [];

    document.querySelectorAll("#weaknesses li").forEach(li => {
        weaknesses.push(["• " + li.innerText]);
    });

    doc.autoTable({
        startY: y,
        body: weaknesses,
        theme: "plain"
    });

    y = doc.lastAutoTable.finalY + 10;

    if (currentMode === "student") {

        const suggestions = document.querySelectorAll("#suggestions li");

        if (suggestions.length) {
            checkPage(55);
            doc.setFontSize(15);

            doc.text("Suggestions", 14, y);

            y += 8;

            const suggestionRows = [];

            suggestions.forEach(li => {

                suggestionRows.push(["• " + li.innerText]);

            });

            doc.autoTable({

                startY: y,

                body: suggestionRows,

                theme: "plain"

            });

            y = doc.lastAutoTable.finalY + 10;

        }
    }

    //=========================
    // Summary
    //=========================

    checkPage(80);

    doc.setTextColor(...dark);

    doc.setFontSize(15);

    doc.text("AI Resume Summary", 14, y);

    y += 8;

    doc.setFontSize(11);

    const summaryText =
        document.getElementById("resumeSummary").innerText;

    const summaryLines =
        doc.splitTextToSize(summaryText, 175);

    doc.text(summaryLines, 18, y, {
        lineHeightFactor: 1.6
    });

    y += summaryLines.length * 6;

    //=========================
    // Footer
    //=========================

    function drawFooter() {

        const pageHeight =
            doc.internal.pageSize.height;

        doc.setFillColor(...blue);

        doc.rect(0, pageHeight - 12, 210, 12, "F");

        doc.setTextColor(255, 255, 255);

        doc.setFontSize(9);

        doc.text(
            "Generated by AI Resume Screening System",
            14,
            pageHeight - 5
        );

        doc.text(
            new Date().toLocaleString(),
            145,
            pageHeight - 5
        );

    }

    const pages = doc.getNumberOfPages();

    for (let i = 1; i <= pages; i++) {

        doc.setPage(i);

        drawFooter();

    }

    doc.save("ATS_Report.pdf");

}

function downloadHRReport() {

    if (!window.hrCandidates) {

        alert("No HR Report Available");

        return;

    }

    let report =
        `========================================
AI RESUME SCREENING REPORT
========================================

`;

    window.hrCandidates.forEach((candidate, index) => {

        report +=
            `
Rank : ${index + 1}

Name : ${candidate.candidate.name}

ATS : ${candidate.score}%

Role : ${candidate.predictedRole}

Recommendation : ${candidate.recommendation}

----------------------------------------

`;

    });

    const blob = new Blob([report], { type: "text/plain" });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "ATS_HR_Report.txt";

    a.click();

    URL.revokeObjectURL(url);

}

// =========================
// EXPORT Excel
// =========================

document.getElementById("exportCSVBtn").addEventListener("click", exportCSV);

async function exportCSV() {

    if (!window.hrCandidates) {
        alert("No Candidates Available");
        return;
    }

    const workbook = new ExcelJS.Workbook();

    const sheet = workbook.addWorksheet("ATS Report");

    // Title
    sheet.mergeCells("A1:E1");
    sheet.getCell("A1").value = "AI Resume Screening System";
    sheet.getCell("A1").font = {
        bold: true,
        size: 18,
        color: { argb: "FFFFFF" }
    };

    sheet.getCell("A1").fill = {
        type: "pattern",
        pattern: "solid",
        fgColor: { argb: "2563EB" }
    };

    sheet.getCell("A1").alignment = {
        horizontal: "center"
    };

    // Subtitle

    sheet.mergeCells("A2:E2");

    sheet.getCell("A2").value = "ATS Candidate Report";

    sheet.getCell("A2").font = {
        bold: true,
        size: 14
    };

    sheet.getCell("A2").alignment = {
        horizontal: "center"
    };

    // Header

    sheet.addRow([]);

    sheet.addRow([
        "Rank",
        "Candidate Name",
        "ATS Score",
        "Role",
        "Recommendation"
    ]);

    const header = sheet.getRow(4);

    header.font = {
        bold: true,
        color: { argb: "FFFFFF" }
    };

    header.fill = {
        type: "pattern",
        pattern: "solid",
        fgColor: { argb: "2563EB" }
    };

    // Candidate rows

    window.hrCandidates.forEach((c, index) => {

        sheet.addRow([
            index + 1,
            c.candidate.name,
            c.score + "%",
            c.predictedRole,
            c.recommendation
        ]);

    });

    // Auto Width

    sheet.columns.forEach(column => {

        let max = 15;

        column.eachCell(cell => {

            max = Math.max(
                max,
                cell.value ? cell.value.toString().length : 10
            );

        });

        column.width = max + 4;

    });

    // Footer

    const last = sheet.lastRow.number + 2;

    sheet.mergeCells(`A${last}:E${last}`);

    sheet.getCell(`A${last}`).value =
        "Generated by AI Resume Screening System";

    sheet.getCell(`A${last}`).font = {
        italic: true
    };

    sheet.mergeCells(`A${last + 1}:E${last + 1}`);

    sheet.getCell(`A${last + 1}`).value =
        new Date().toLocaleString();

    // Download

    const buffer = await workbook.xlsx.writeBuffer();

    const blob = new Blob(
        [buffer],
        {
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "ATS_Candidate_Report.xlsx";

    a.click();

    URL.revokeObjectURL(url);

}




updateSidebar();
switchHRMode();
