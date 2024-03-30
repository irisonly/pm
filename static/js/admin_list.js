import { END_POINT } from "./config.js";

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

const promise_type = fetch(END_POINT + "/admin", {
  method: "GET",
  headers: { Authorization: "Bearer " + get_token() },
})
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    const content = data.response;
    console.log(content);
    const member_list = document.getElementById("m_container");
    member_list.innerHTML = "";
    content.forEach(element => {
      const data_list = document.createElement("ul");
      data_list.className = "m_projects";
      data_list.innerHtml = "";
      member_list.appendChild(data_list);
      const name = document.createElement("li");
      data_list.appendChild(name);
      const name_edit = document.createElement("a");
      name_edit.id = element.id;
      name_edit.textContent = element.admin;
      name_edit.href = "./admin_detail.html?id=" + element.id;
      name_edit.className = "project_name";
      name.appendChild(name_edit);

      const m_project = document.createElement("li");
      m_project.style.width = "1000px";
      const projects = element.projects.map(project => project.name).join(" ");
      m_project.textContent = projects;
      data_list.appendChild(m_project);
    });
  })
  .catch(error => {
    console.error("请求失败:", error);
    // window.location.href = "./login.html";
  });
