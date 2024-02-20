import { END_POINT } from "./config.js";

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

function add_cost() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const _id = urlParams.get("id");
  fetch(END_POINT + "/cost?id=" + _id, {
    method: "GET",
    // headers: { Authorization: "Bearer " + get_token() },
  })
    .then(response => response.json())
    .then(data => {
      if (data == null) {
        return;
      }
      add_cost_column(data["response"]);
    })
    .catch(error => console.error("请求失败:", error));
}

function list_render(data) {
  const container = document.getElementById("container");
  container.innerHTML = "";
  const element = data.response;
  console.log(element);
  const data_list = document.createElement("ul");
  data_list.className = "projects";
  data_list.innerHtml = "";
  container.appendChild(data_list);
  const name = document.createElement("li");
  data_list.appendChild(name);
  const name_edit = document.createElement("a");
  name_edit.id = element.id;
  name_edit.textContent = element.name;
  name_edit.href = "./detail.html?id=" + element.id;
  name_edit.className = "project_name";
  if (name_edit.innerText.length > 10) {
    name_edit.innerText = name_edit.innerText.slice(0, 10);
  }
  name.appendChild(name_edit);
  const type_id = document.createElement("li");
  type_id.textContent = element.type_id;
  data_list.appendChild(type_id);
  const status_id = document.createElement("li");
  status_id.textContent = element.status_id;
  data_list.appendChild(status_id);
  const payment = document.createElement("li");
  payment.textContent = element.payment;
  data_list.appendChild(payment);
  const cost = document.createElement("li");
  cost.textContent = element.cost;
  data_list.appendChild(cost);
  const tax = document.createElement("li");
  tax.textContent = element.tax;
  data_list.appendChild(tax);
  const profit = document.createElement("li");
  profit.textContent = element.profit;
  data_list.appendChild(profit);
  const profit_rate = document.createElement("li");
  profit_rate.textContent = element.profit_rate;
  data_list.appendChild(profit_rate);
  const charge_id = document.createElement("li");
  let charge_id_text = "";
  element.m_charges.forEach(element => {
    charge_id_text += element.charge + " ";
  });
  charge_id.textContent = charge_id_text;
  data_list.appendChild(charge_id);
  const charge_id_p = document.createElement("li");
  let charge_id_text_p = "";
  element.p_charges.forEach(element => {
    charge_id_text_p += element.charge + " ";
  });
  charge_id_p.textContent = charge_id_text_p;
  data_list.appendChild(charge_id_p);
  const start_time = document.createElement("li");
  start_time.textContent = element.start_time;
  data_list.appendChild(start_time);
  const end_time = document.createElement("li");
  end_time.textContent = element.end_time;
  data_list.appendChild(end_time);
}

function add_cost_column(data) {
  const container = document.getElementById("c_container");
  container.innerHTML = "";
  data.forEach(element => {
    const data_list = document.createElement("ul");
    data_list.className = "projects";
    data_list.innerHtml = "";
    container.appendChild(data_list);
    const li = document.createElement("li");
    li.innerHTML = element.id;
    data_list.appendChild(li);
    const li1 = document.createElement("li");
    li1.innerHTML = element.name;
    data_list.appendChild(li1);
    const li2 = document.createElement("li");
    li2.innerHTML = element.cost;
    data_list.appendChild(li2);
    const li3 = document.createElement("li");
    li3.innerHTML = element.remark;
    data_list.appendChild(li3);
    const li4 = document.createElement("li");
    data_list.appendChild(li4);
    const a = document.createElement("a");
    a.textContent = "删除";
    a.href = "#";
    a.dataset.id = element.id;
    a.addEventListener("click", e => {
      const _id = parseInt(e.target.dataset.id, 10);
      console.log(_id);
      e.preventDefault();
      fetch(END_POINT + "/cost", {
        method: "DELETE", // 指定请求方法为 POST
        headers: {
          // 指定发送的数据类型为 JSON
          "Content-Type": "application/json",
          //   Authorization: "Bearer " + refresh_token,
        },
        body: JSON.stringify({ id: _id }), // 将 JavaScript 对象转换为 JSON 字符串
      })
        .then(response => response.json()) // 解析 JSON 响应
        .then(data => {
          console.log(data);
        })
        .catch(error => {
          console.error("Error:", error);
          alert("获取失败，请检查");
        });
    });

    li4.appendChild(a);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  add_cost();
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const _id = urlParams.get("id");

  fetch(END_POINT + "/project?name&charge_p_id&type_id&charge_m_id&id=" + _id, {
    method: "GET",
    headers: { Authorization: "Bearer " + get_token() },
  })
    .then(response => response.json()) // 将响应转换为JSON
    .then(data => {
      list_render(data);
    })
    .catch(error => {
      console.error("请求失败:", error);
    });

  const form = document.getElementById("cost_form");
  form.addEventListener("submit", e => {
    e.preventDefault();
    const form_data = new FormData(form);
    const form_api = {};
    form_data.forEach((value, key) => {
      form_api[key] = value;
    });
    form_api["project_id"] = parseInt(_id, 10);
    form_api["cost"] = parseFloat(form_api["cost"], 10);
    console.log(form_api);
    fetch(END_POINT + "/cost", {
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
        console.log("Success:", form_api);
      })
      .catch(error => {
        console.error("Error:", error);
        alert("项目创建失败，请检查");
      });
  });
});
