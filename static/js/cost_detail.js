import { END_POINT } from "./config.js";

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

function select_default(select_id, default_value) {
  type_select(
    [
      { id: 0, name: "未支付" },
      { id: 1, name: "已支付" },
    ],
    "status"
  );
  const select = document.getElementById(select_id);
  const sel = select.options;
  Array.from(sel).forEach((ele, ind) => {
    // console.log(ele.value, default_value);
    if (ele.value == default_value) {
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

document.addEventListener("DOMContentLoaded", () => {
  const query_string = window.location.search;
  const query_url = new URLSearchParams(query_string);
  const id = query_url.get("id");
  const c_id = query_url.get("c_id");
  const back_btn = document.getElementById("cost_back");
  back_btn.href = "./cost.html?id=" + id;
  fetch(END_POINT + "/cost?id=" + id + "&c_id=" + c_id, {
    method: "GET",
    headers: { Authorization: "Bearer " + get_token() },
  })
    .then(response => response.json()) // 将响应转换为JSON
    .then(data => {
      const content = data.response;
      console.log(content);
      const name = document.getElementById("name");
      name.value = content.name;
      select_default("status", content.status);
      const cost = document.getElementById("cost");
      cost.value = content.cost;
      const remark = document.getElementById("remark");
      remark.value = content.remark;
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
    form_api["cost"] = parseFloat(form_api["cost"], 10);
    form_api["id"] = parseInt(c_id, 10);
    form_api["status"] = parseInt(form_api["status"], 10);
    console.log(form_api);
    fetch(END_POINT + "/cost", {
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
        window.location.href = "./cost.html?id=" + id;
      })
      .catch(error => {
        console.error("Error:", error);
        alert("数据更新失败，请检查");
      });
  });
});
