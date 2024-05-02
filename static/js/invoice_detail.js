import { END_POINT } from "./config.js";

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

function select_default_m(select_id, default_value) {
  type_select(
    [
      { id: 1, name: "1" },
      { id: 2, name: "2" },
      { id: 3, name: "3" },
      { id: 4, name: "4" },
      { id: 5, name: "5" },
      { id: 6, name: "6" },
      { id: 7, name: "7" },
      { id: 8, name: "8" },
      { id: 9, name: "9" },
      { id: 10, name: "10" },
      { id: 11, name: "11" },
      { id: 12, name: "12" },
    ],
    "month"
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

function select_default_s(select_id, default_value) {
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
  back_btn.href = "./invoice.html?id=" + id;
  fetch(END_POINT + "/invoice?id=" + id + "&c_id=" + c_id, {
    method: "GET",
    headers: { Authorization: "Bearer " + get_token() },
  })
    .then(response => response.json()) // 将响应转换为JSON
    .then(data => {
      const content = data.response;
      console.log(content);
      const name = document.getElementById("name");
      name.value = content.name;

      select_default_m("month", content.month);
      const invoice = document.getElementById("invoice");
      invoice.value = content.invoice;
      const remark = document.getElementById("remark");
      remark.value = content.remark;
    })
    .catch(error => {
      console.error("请求失败:", error);
      window.location.href = "./login.html";
    });

  const form = document.getElementById("project_form");

  form.addEventListener("submit", e => {
    e.preventDefault();
    const form_data = new FormData(form);
    const form_api = {};
    form_data.forEach((value, key) => {
      form_api[key] = value;
    });
    form_api["invoice"] = parseFloat(form_api["invoice"], 10);
    form_api["id"] = parseInt(c_id, 10);
    form_api["month"] = parseInt(form_api["month"], 10);

    console.log(form_api);
    fetch(END_POINT + "/invoice", {
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
        window.location.href = "./invoice.html?id=" + id;
      })
      .catch(error => {
        console.error("Error:", error);
        alert("数据更新失败，请检查");
      });
  });
});
