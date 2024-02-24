import { END_POINT } from "./config.js";

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

function select_default(select_id, default_value) {
  const select = document.getElementById(select_id);
  const sel = select.options;
  Array.from(sel).forEach((ele, ind) => {
    if (ele.textContent == default_value) {
      select.selectedIndex = ind;
    }
  });
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

function handle_delete(event) {
  const query_string = window.location.search;
  const query_url = new URLSearchParams(query_string);
  const name = query_url.get("name");
  console.log(event, name);
  fetch(END_POINT + "/charge?name=" + name, {
    method: "DELETE", // 指定请求方法为 POST
    headers: {
      // 指定发送的数据类型为 JSON
      "Content-Type": "application/json",
    },
  })
    .then(response => response.json()) // 解析 JSON 响应
    .then(data => {
      console.log("Success:", name);
      // alert("项目删除成功");
      window.location.href = "./member.html";
    })
    .catch(error => {
      console.error("Error:", error);
      alert("项目删除失败，请检查");
    });
}

fetch(END_POINT + "/level", {
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
  const query_string = window.location.search;
  const query_url = new URLSearchParams(query_string);
  const id = query_url.get("id");

  const name = query_url.get("name");
  fetch(END_POINT + "/charge?name=" + name, {
    method: "GET",
    headers: { Authorization: "Bearer " + get_token() },
  })
    .then(response => response.json()) // 将响应转换为JSON
    .then(data => {
      const content = data.response;
      console.log(content);
      const name = document.getElementById("name");
      name.value = content.name;
      select_default("status_id", content.level);
      const salary = document.getElementById("salary");
      salary.value = content.salary;
    })
    .catch(error => {
      console.error("请求失败:", error);
      // window.location.href = "./login.html";
    });

  const form = document.getElementById("project_form");

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
      method: "PUT", // 指定请求方法为 POST
      headers: {
        // 指定发送的数据类型为 JSON
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form_api), // 将 JavaScript 对象转换为 JSON 字符串
    })
      .then(response => response.json()) // 解析 JSON 响应
      .then(data => {
        console.log("Success:", form_api);
        alert("数据更新完成");
        window.location.href = "./member.html";
      })
      .catch(error => {
        console.error("Error:", error);
        alert("数据更新失败，请检查");
      });
  });

  const del_btn = document.getElementById("delete_project");
  del_btn.addEventListener("click", handle_delete);
  // 使用 fetch 发起 POST 请求
});
