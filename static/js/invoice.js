import { END_POINT } from "./config.js";

let project_type = [];
let project_status = [];

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

function add_cost() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const _id = urlParams.get("id");
  fetch(END_POINT + "/invoice?id=" + _id, {
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

function upload() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const _id = urlParams.get("id");
  const input = document.getElementById("excelFile");
  console.log(input);
  const file = input.files[0];
  console.log(file);
  if (file) {
    // 使用FormData来包装文件数据
    const formData = new FormData();
    formData.append("file", file);
    // 发起POST请求到后端API
    fetch(END_POINT + "/import?id=" + _id, {
      method: "POST",
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        window.location.reload();
      })
      .catch(error => console.error("Error:", error));
  } else {
    alert("Please select a file.");
  }
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
  const type_id_text = project_type.find(e => e.id == element.type_id).name;
  type_id.textContent = type_id_text;
  data_list.appendChild(type_id);
  const status_id = document.createElement("li");
  const status_id_text = project_status.find(
    e => e.id == element.status_id
  ).name;
  status_id.textContent = status_id_text;
  data_list.appendChild(status_id);
  const payment = document.createElement("li");
  payment.textContent = element.payment;
  data_list.appendChild(payment);
  const balance_payment = document.createElement("li");
  balance_payment.textContent = element.balance_payment;
  data_list.appendChild(balance_payment);
  const cost = document.createElement("li");
  cost.textContent = element.cost;
  data_list.appendChild(cost);
  const not_paid = document.createElement("li");
  not_paid.textContent = element.not_paid;
  data_list.appendChild(not_paid);
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
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const pid = urlParams.get("id");
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
    li2.innerHTML = element.invoice;
    data_list.appendChild(li2);
    const li_tax = document.createElement("li");
    li_tax.innerHTML = element.invoice_tax;
    data_list.appendChild(li_tax);
    const li6 = document.createElement("li");
    li6.innerHTML = element.month + "月";
    data_list.appendChild(li6);
    const li3 = document.createElement("li");
    li3.innerHTML = element.remark;
    data_list.appendChild(li3);
    const li4 = document.createElement("li");
    data_list.appendChild(li4);
    const a2 = document.createElement("a");
    a2.textContent = "删除";
    a2.href = "#";
    a2.dataset.id = element.id;
    a2.addEventListener("click", e => {
      const _id = parseInt(e.target.dataset.id, 10);
      console.log(_id);
      e.preventDefault();
      fetch(END_POINT + "/invoice", {
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
          alert("删除成功");
          console.log(data);
          location.reload();
        })
        .catch(error => {
          console.error("Error:", error);
          alert("获取失败，请检查");
        });
    });
    li4.appendChild(a2);
    const a1 = document.createElement("a");
    a1.textContent = " 修改";
    a1.href =
      "./invoice_detail.html?id=" + element.project_id + "&c_id=" + element.id;
    li4.appendChild(a1);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  add_cost();
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const _id = urlParams.get("id");
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
  fetch(END_POINT + "/type", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + get_token(),
    },
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      project_type = data.response;
      return fetch(END_POINT + "/status", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + get_token(),
        },
      });
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      project_status = data.response;
      return fetch(
        END_POINT + "/project?name&charge_p_id&type_id&charge_m_id&id=" + _id,
        {
          method: "GET",
          headers: { Authorization: "Bearer " + get_token() },
        }
      );
    })
    .then(response => response.json())
    .then(data => {
      list_render(data);
    })
    .catch(error => {
      console.error("请求失败:", error);
      // window.location.href = "./login.html";
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
    form_api["invoice"] = parseFloat(form_api["invoice"], 10);
    form_api["month"] = parseInt(form_api["month"], 10);
    console.log(form_api);
    fetch(END_POINT + "/invoice", {
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
        location.reload();
        console.log("Success:", form_api);
      })
      .catch(error => {
        console.error("Error:", error);
        alert("项目创建失败，请检查");
      });
  });
});
