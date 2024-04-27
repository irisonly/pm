import { END_POINT, super_admin } from "./config.js";

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

function dashboard_render(data) {
  const date = new Date();
  const month = date.getMonth() + 1;
  if (super_admin.includes(localStorage.getItem("id"))) {
    const response = data;
    console.log(response);
    const dash_list = document.getElementById("dash_list");
    dash_list.innerHTML = "";
    const sum_of_payment_title = document.createElement("li");
    sum_of_payment_title.textContent = "总营业额";
    const sum_of_payment = document.createElement("li");
    sum_of_payment.textContent = response.sum_of_payment;
    const sum_of_profit_title = document.createElement("li");
    sum_of_profit_title.textContent = "总利润";
    const sum_of_profit = document.createElement("li");
    sum_of_profit.textContent = response.sum_of_profit;
    const sum_of_balance_payment_title = document.createElement("li");
    sum_of_balance_payment_title.textContent = "应收账款";
    const sum_of_balance_payment = document.createElement("li");
    sum_of_balance_payment.textContent = response.sum_of_balance_payment;
    const sum_of_salary_title = document.createElement("li");
    sum_of_salary_title.textContent = "总人员成本";
    const sum_of_salary = document.createElement("li");
    sum_of_salary.textContent = response.sum_of_salary;
    const sum_of_cost_title = document.createElement("li");
    sum_of_cost_title.textContent = "当月应付成本";
    const sum_of_cost = document.createElement("li");
    sum_of_cost.textContent = response.sum_of_cost;
    dash_list.appendChild(sum_of_payment_title);
    dash_list.appendChild(sum_of_payment);
    dash_list.appendChild(sum_of_profit_title);
    dash_list.appendChild(sum_of_profit);
    dash_list.appendChild(sum_of_balance_payment_title);
    dash_list.appendChild(sum_of_balance_payment);
    dash_list.appendChild(sum_of_salary_title);
    dash_list.appendChild(sum_of_salary);
    dash_list.appendChild(sum_of_cost_title);
    dash_list.appendChild(sum_of_cost);
  }
}

function add_cost() {
  const date = new Date();
  const month = date.getMonth() + 1;
  fetch(END_POINT + "/costoverall?month=" + month, {
    method: "GET",
    // headers: { Authorization: "Bearer " + get_token() },
  })
    .then(response => response.json())
    .then(data => {
      if (data == null) {
        return;
      }
      add_cost_column(data["response"]);
      dashboard_render(data.response[0].dashboard);
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

function submit_form(event) {
  event.preventDefault();
  const form = event.target;
  const form_data = new FormData(form);
  const query_string = new URLSearchParams(form_data).toString();
  // console.log(query_string);
  fetch(END_POINT + "/costoverall?" + query_string, {
    method: "GET",
    headers: { Authorization: "Bearer " + get_token() },
  })
    .then(response => response.json())
    .then(data => {
      if (data == null) {
        add_cost_column([]);
      }
      add_cost_column(data["response"]);
      if (data.response[0].dashboard != undefined) {
        dashboard_render(data.response[0].dashboard);
      }
    })
    .catch(error => console.error("请求失败:", error));
}

function reset_form(event) {
  event.preventDefault();
  add_cost();
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
  if (data.length == 0) {
    return;
  }
  data.forEach(element => {
    const data_list = document.createElement("ul");
    data_list.className = "projects";
    data_list.innerHtml = "";
    container.appendChild(data_list);
    const li = document.createElement("li");
    li.innerHTML = element.id;
    data_list.appendChild(li);
    const li10 = document.createElement("li");
    li10.innerHTML = element.project;
    data_list.appendChild(li10);
    const li1 = document.createElement("li");
    li1.innerHTML = element.name;
    data_list.appendChild(li1);
    const li2 = document.createElement("li");
    li2.innerHTML = element.cost;
    data_list.appendChild(li2);
    const li6 = document.createElement("li");
    li6.innerHTML = element.month + "月";
    data_list.appendChild(li6);
    const li3 = document.createElement("li");
    li3.innerHTML = element.remark;
    data_list.appendChild(li3);

    const li5 = document.createElement("li");
    if (element.status == 0) {
      li5.innerHTML = "未支付";
    } else {
      li5.innerHTML = "已支付";
    }
    // li5.innerHTML = element.status;
    data_list.appendChild(li5);
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
      fetch(END_POINT + "/cost", {
        method: "DELETE", // 指定请求方法为 POST
        headers: {
          // 指定发送的数据类型为 JSON
          "Content-Type": "application/json",
          //   Authorization: "Bearer " + refresh_token,
        },
        body: JSON.stringify({ id: _id, pid: pid }), // 将 JavaScript 对象转换为 JSON 字符串
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
      "./cost_detail.html?id=" + element.project_id + "&c_id=" + element.id;
    li4.appendChild(a1);
  });
}

// fetch(END_POINT + "/dashboard", {
//   method: "GET",
//   headers: { Authorization: "Bearer " + get_token() },
// })
//   .then(response => response.json()) // 将响应转换为JSON
//   .then(data => {
//     const default_dashborad = data.response;
//     dashboard_render(data.response);
//   })
//   .catch(error => {
//     console.error("请求失败:", error);
//     // window.location.href = "./login.html";
//   });

document.addEventListener("DOMContentLoaded", function () {
  type_select(
    [
      { id: 13, name: "全部" },
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
  add_cost();
  document.getElementById("query_form").addEventListener("submit", submit_form);
  document.getElementById("query_form").addEventListener("reset", reset_form);
});