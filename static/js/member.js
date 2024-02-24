import { END_POINT } from "./config.js";

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

function type_select(data, _id) {
  const response = data;
  const select_form = document.getElementById(_id);
  response.forEach(element => {
    const opt = document.createElement("option");
    opt.value = element.id;
    opt.textContent = element.name;
    select_form.appendChild(opt);
  });
}

const promise_type = fetch(END_POINT + "/charge", {
  method: "GET",
  headers: { Authorization: "Bearer " + get_token() },
})
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    const content = data.response;
    console.log(content);
    const member_list = document.getElementById("container");
    member_list.innerHTML = "";
    content.forEach(element => {
      const data_list = document.createElement("ul");
      data_list.className = "projects";
      data_list.innerHtml = "";
      member_list.appendChild(data_list);
      const name = document.createElement("li");
      data_list.appendChild(name);
      const name_edit = document.createElement("a");
      name_edit.id = element.id;
      name_edit.textContent = element.name;
      name_edit.href = "./member_detail.html?name=" + element.name;
      name_edit.className = "project_name";
      name.appendChild(name_edit);
      const position = document.createElement("li");
      position.textContent = element.level;
      data_list.appendChild(position);
      const salary = document.createElement("li");
      salary.textContent = element.salary;
      data_list.appendChild(salary);
      const m_project = document.createElement("li");
      m_project.style.width = "500px";
      const projects = element.m_projects.map(project => project).join(" ");
      m_project.textContent = projects;
      data_list.appendChild(m_project);
      const p_project = document.createElement("li");
      p_project.style.width = "500px";
      const p_projects = element.p_projects.map(project => project).join(" ");
      p_project.textContent = p_projects;
      data_list.appendChild(p_project);
    });
  })
  .catch(error => {
    console.error("请求失败:", error);
    // window.location.href = "./login.html";
  });

const promise_level = fetch(END_POINT + "/level", {
  method: "GET",
  // headers: { Authorization: "Bearer " + get_token() },
})
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    const content = data.response;
    console.log(content);
    type_select(content, "status_id");
  })
  .catch(error => {
    console.error("请求失败:", error);
    // window.location.href = "./login.html";
  });

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("cost_form");
  form.addEventListener("submit", e => {
    e.preventDefault();
    const form_data = new FormData(form);
    const form_api = {};
    form_data.forEach((value, key) => {
      form_api[key] = value;
    });
    form_api["level"] = parseInt(form_api["level"], 10);
    form_api["salary"] = parseFloat(form_api["salary"]);
    console.log(form_api);
    fetch(END_POINT + "/charge", {
      method: "POST", // 指定请求方法为 POST
      headers: {
        // 指定发送的数据类型为 JSON
        "Content-Type": "application/json",
        // Authorization: "Bearer " + get_token(),
      },
      body: JSON.stringify(form_api), // 将 JavaScript 对象转换为 JSON 字符串
    })
      .then(response => response.json()) // 解析 JSON 响应
      .then(data => {
        alert("添加成功");
        console.log("Success:", form_api);
      })
      .catch(error => {
        console.error("Error:", error);
        alert("项目创建失败，请检查");
      });
  });
});
