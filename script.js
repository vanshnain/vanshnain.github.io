const students = [
  {
    name: "Vansh Nain",
    dob: "07/06/2006",
    Email: "vansh.nain@ramanujan.du.ac.in",
    username: "vansh.nain",
    password: "vansh@0087",
    attendance: 76.79,
    subjects: [
      { name: "HTML", code: "BCA101", faculty: "Ms. Sharma" },
      { name: "C++", code: "BCA102", faculty: "Mr. Mehta" },
      { name: "DBMS", code: "BCA103", faculty: "Dr. Verma" },
      { name: "CN", code: "BCA104", faculty: "Ms. Kaur" }
    ],
    assignments: [
      { title: "HTML Website Layout", subject: "HTML", status: "Pending" },
      { title: "C++ OOP Program", subject: "C++", status: "Submitted" },
      { title: "DBMS Table Design", subject: "DBMS", status: "Pending" },
      { title: "OSI Model Report", subject: "CN", status: "Submitted" }
    ],
    results: [
      { subject: "HTML", marks: 78, grade: "B+" },
      { subject: "C++", marks: 82, grade: "A" },
      { subject: "DBMS", marks: 75, grade: "B+" },
      { subject: "CN", marks: 80, grade: "A" }
    ],
    fees: [
      { type: "Tuition Fee", amount: "₹25,000", status: "Paid" },
      { type: "Library Fee", amount: "₹2,000", status: "Paid" },
      { type: "Exam Fee", amount: "₹3,500", status: "Pending" }
    ],
    notices: [
      "Website project submission deadline is 31 March 2026.",
      "Mid-sem practical schedule will be released next week.",
      "Carry your college ID for all lab sessions."
    ]
  },
  {
    name: "Shivansh Pandey",
    dob: "14/02/2006",
    Email: "shivansh.pandey@ramanujan.du.ac.in",
    username: "shivansh.pandey",
    password: "shivansh@0060",
    attendance: 86.1,
    subjects: [
      { name: "HTML", code: "BCA101", faculty: "DR. Kamlesh" },
      { name: "C++", code: "BCA102", faculty: "Mr. Rathi" },
      { name: "DBMS", code: "BCA103", faculty: "Ms. Sheetal" },
      { name: "CN", code: "BCA104", faculty: "Ms. Sheetal" }
    ],
    assignments: [
      { title: "HTML Forms Assignment", subject: "HTML", status: "Submitted" },
      { title: "C++ Inheritance Program", subject: "C++", status: "Submitted" },
      { title: "Normalization Exercise", subject: "DBMS", status: "Pending" },
      { title: "Network Topology Chart", subject: "CN", status: "Submitted" }
    ],
    results: [
      { subject: "HTML", marks: 88, grade: "A" },
      { subject: "C++", marks: 91, grade: "A+" },
      { subject: "DBMS", marks: 84, grade: "A" },
      { subject: "CN", marks: 86, grade: "A" }
    ],
    fees: [
      { type: "Tuition Fee", amount: "₹25,000", status: "Paid" },
      { type: "Library Fee", amount: "₹2,000", status: "Paid" },
      { type: "Exam Fee", amount: "₹3,500", status: "Paid" }
    ],
    notices: [
      "Internal assessment marks have been uploaded.",
      "DBMS viva will be conducted on Friday.",
      "Attendance above 75% is mandatory for exams."
    ]
  },
  {
    name: "Mayank Kataria",
    dob: "18/08/2006",
    Email: "mayank.kataria@ramanujan.du.ac.in",
    username: "mayank.kataria",
    password: "mayank@0037",
    attendance: 56.79,
    subjects: [
      { name: "HTML", code: "BCA101", faculty: "Ms. Sharma" },
      { name: "C++", code: "BCA102", faculty: "Mr. Mehta" },
      { name: "DBMS", code: "BCA103", faculty: "Dr. Verma" },
      { name: "CN", code: "BCA104", faculty: "Ms. Kaur" }
    ],
    assignments: [
      { title: "HTML Landing Page", subject: "HTML", status: "Pending" },
      { title: "C++ Arrays Program", subject: "C++", status: "Pending" },
      { title: "SQL Query File", subject: "DBMS", status: "Submitted" },
      { title: "Computer Networks Basics", subject: "CN", status: "Pending" }
    ],
    results: [
      { subject: "HTML", marks: 60, grade: "C+" },
      { subject: "C++", marks: 58, grade: "C" },
      { subject: "DBMS", marks: 67, grade: "B" },
      { subject: "CN", marks: 61, grade: "C+" }
    ],
    fees: [
      { type: "Tuition Fee", amount: "₹25,000", status: "Paid" },
      { type: "Library Fee", amount: "₹2,000", status: "Pending" },
      { type: "Exam Fee", amount: "₹3,500", status: "Pending" }
    ],
    notices: [
      "Low attendance students must meet the class coordinator.",
      "Submit pending assignments before the final review.",
      "Computer Networks class test is scheduled next Monday."
    ]
  }
];

function getCurrentStudent() {
  const username = localStorage.getItem("loggedInUser");
  return students.find(s => s.username === username);
}

function requireLogin() {
  const student = getCurrentStudent();
  if (!student) {
    window.location.href = "login.html";
    return null;
  }
  return student;
}

function logout() {
  localStorage.removeItem("loggedInUser");
  window.location.href = "login.html";
}

function setupLogin() {
  const form = document.getElementById("loginForm");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorMessage = document.getElementById("errorMessage");

    const student = students.find(
      s => s.username === username && s.password === password
    );

    if (student) {
      localStorage.setItem("loggedInUser", student.username);
      window.location.href = "dashboard.html";
    } else {
      errorMessage.textContent = "Invalid username or password.";
    }
  });
}

function fillCommon(student) {
  const map = {
    topWelcome: `Welcome back, ${student.name}`,
    topBadge: student.username,
    studentName: student.name,
    studentUsername: student.username,
    detailName: student.name,
    detailDob: student.dob,
    detailUsername: student.username,
    profileName: student.name,
    profileDob: student.dob,
    profileUsername: student.username
  };

  Object.keys(map).forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = map[id];
  });

  const avatar = document.getElementById("profileAvatar");
  if (avatar) avatar.textContent = student.name.charAt(0).toUpperCase();
}

function fillAttendance(student) {
  const percentEls = ["attendancePercent", "attendancePercentPage"];
  const barEls = ["attendanceBar", "attendanceBarPage"];
  const statusEls = ["attendanceStatus", "attendanceStatusPage"];

  percentEls.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = student.attendance + "%";
  });

  barEls.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.width = student.attendance + "%";
  });

  let label = "Low";
  let className = "low";

  if (student.attendance >= 75) {
    label = "Good";
    className = "good";
  } else if (student.attendance >= 60) {
    label = "Average";
    className = "average";
  }

  statusEls.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = label;
      el.className = className;
    }
  });
}

function fillSubjects(student) {
  const tbody = document.getElementById("subjectsTableBody");
  if (!tbody) return;

  tbody.innerHTML = student.subjects.map((subject, index) => `
    <tr>
      <td>${index + 1}</td>
      <td>${subject.name}</td>
      <td>${subject.code}</td>
      <td>${subject.faculty}</td>
    </tr>
  `).join("");
}

function fillAssignments(student) {
  const tbody = document.getElementById("assignmentsTableBody");
  if (!tbody) return;

  tbody.innerHTML = student.assignments.map((assignment, index) => `
    <tr>
      <td>${index + 1}</td>
      <td>${assignment.title}</td>
      <td>${assignment.subject}</td>
      <td><span class="assignment-status ${assignment.status.toLowerCase()}">${assignment.status}</span></td>
      <td><a href="#" class="download-link">Download</a></td>
    </tr>
  `).join("");
}

function fillResults(student) {
  const tbody = document.getElementById("resultsTableBody");
  if (!tbody) return;

  tbody.innerHTML = student.results.map(result => `
    <tr>
      <td>${result.subject}</td>
      <td>${result.marks}</td>
      <td>${result.grade}</td>
    </tr>
  `).join("");
}

function fillFees(student) {
  const tbody = document.getElementById("feesTableBody");
  if (!tbody) return;

  tbody.innerHTML = student.fees.map(fee => `
    <tr>
      <td>${fee.type}</td>
      <td>${fee.amount}</td>
      <td><span class="fee-status ${fee.status.toLowerCase() === "paid" ? "paid" : "unpaid"}">${fee.status}</span></td>
    </tr>
  `).join("");
}

function fillNotices(student) {
  const listIds = ["noticeList", "noticeListDashboard"];
  listIds.forEach(id => {
    const ul = document.getElementById(id);
    if (ul) {
      ul.innerHTML = student.notices.map(n => `<li>${n}</li>`).join("");
    }
  });
}

function initPage() {
  setupLogin();

  const protectedPages = [
    "dashboard.html",
    "profile.html",
    "subjects.html",
    "attendance.html",
    "assignments.html",
    "results.html",
    "fees.html",
    "notice.html"
  ];

  const currentPage = window.location.pathname.split("/").pop();
  if (!protectedPages.includes(currentPage)) return;

  const student = requireLogin();
  if (!student) return;

  fillCommon(student);
  fillAttendance(student);
  fillSubjects(student);
  fillAssignments(student);
  fillResults(student);
  fillFees(student);
  fillNotices(student);
}

document.addEventListener("DOMContentLoaded", initPage);
