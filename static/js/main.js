import { END_POINT } from "./config.js";

function list_render(data) {
  if (Array.isArray(data.response)) {
    const container = document.getElementById("container");
    container.innerHTML = "";
    const response = data.response;
    console.log(response);
    response.forEach(element => {
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
      data_list.appendChild(cost);
      const cost_edit = document.createElement("a");
      cost_edit.id = element.id;
      cost_edit.textContent = element.cost;
      cost_edit.href = "./cost.html?id=" + element.id;
      cost.appendChild(cost_edit);
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
    });
  } else {
    const container = document.getElementById("container");
    container.innerHTML = "";
  }
}

function dashboard_render(data) {
  const response = data.response;
  console.log(response);
  const dash_list = document.getElementById("dash_list");
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
  dash_list.appendChild(sum_of_payment_title);
  dash_list.appendChild(sum_of_payment);
  dash_list.appendChild(sum_of_profit_title);
  dash_list.appendChild(sum_of_profit);
  dash_list.appendChild(sum_of_balance_payment_title);
  dash_list.appendChild(sum_of_balance_payment);
  dash_list.appendChild(sum_of_salary_title);
  dash_list.appendChild(sum_of_salary);
}

function type_select(data, _id) {
  const response = data.response;
  console.log(response);
  const select_form = document.getElementById(_id);
  const opt = document.createElement("option");
  opt.value = "";
  opt.textContent = "全部";
  select_form.appendChild(opt);
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
  fetch(END_POINT + "/project?id&" + query_string, {
    method: "GET",
    headers: { Authorization: "Bearer " + get_token() },
  })
    .then(response => response.json()) // 将响应转换为JSON
    .then(data => {
      list_render(data);
    })
    .catch(error => console.error("请求失败:", error));
}

function reset_form(event) {
  event.preventDefault();
  fetch(END_POINT + "/projectlist", {
    method: "GET",
    headers: { Authorization: "Bearer " + get_token() },
  })
    .then(response => response.json()) // 将响应转换为JSON
    .then(data => {
      list_render(data);
      reset_query();
    })
    .catch(error => console.error("请求失败:", error));
}

function reset_query() {
  document.getElementById("type").selectedIndex = 0;
  document.getElementById("m_charge").selectedIndex = 0;
  document.getElementById("p_charge").selectedIndex = 0;
  document.getElementById("project_name").value = "";
}

function click(event) {
  event.preventDefault();
  const id = parseInt(event.target.id, 10);
  fetch(END_POINT + "/project?name&charge_id&type_id&id=" + id)
    .then(response => response.json()) // 将响应转换为JSON
    .then(data => {
      console.log(data);
    })
    .catch(error => console.error("请求失败:", error));
}

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

function refresh_token() {
  refresh_token = localStorage.getItem("refresh_token");
  fetch(END_POINT + "/refresh", {
    method: "POST", // 指定请求方法为 POST
    headers: {
      // 指定发送的数据类型为 JSON
      "Content-Type": "application/json",
      Authorization: "Bearer " + refresh_token,
    },
    body: JSON.stringify(form_api), // 将 JavaScript 对象转换为 JSON 字符串
  })
    .then(response => response.json()) // 解析 JSON 响应
    .then(data => {
      localStorage.setItem("access_token", data["response"]["access_token"]);
    })
    .catch(error => {
      console.error("Error:", error);
      alert("获取失败，请检查");
    });
}

fetch(END_POINT + "/projectlist", {
  method: "GET",
  headers: { Authorization: "Bearer " + get_token() },
})
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    list_render(data);
  })
  .catch(error => {
    console.error("请求失败:", error);
    window.location.href = "./login.html";
  });

fetch(END_POINT + "/dashboard", {
  method: "GET",
  headers: { Authorization: "Bearer " + get_token() },
})
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    dashboard_render(data);
  })
  .catch(error => {
    console.error("请求失败:", error);
    window.location.href = "./login.html";
  });

fetch(END_POINT + "/charge")
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    type_select(data, "m_charge");
  })
  .catch(error => console.error("请求失败:", error));

fetch(END_POINT + "/charge")
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    type_select(data, "p_charge");
  })
  .catch(error => console.error("请求失败:", error));

fetch(END_POINT + "/type", {
  method: "GET",
  headers: { Authorization: "Bearer " + get_token() },
})
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    type_select(data, "type");
  })
  .catch(error => console.error("请求失败:", error));

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("query_form").addEventListener("submit", submit_form);
  document.getElementById("query_form").addEventListener("reset", reset_form);
  document.getElementById("excel").addEventListener("click", e => {
    e.preventDefault();
    fetch(END_POINT + "/excel", {
      method: "GET",
    })
      .then(response => {
        return response.blob();
      }) // 将响应转换为JSON
      .then(data => {
        console.log(data);
        const url = window.URL.createObjectURL(data);
        const a = document.createElement("a");
        a.href = url;
        a.download = "project.xlsx";
        a.click();
        window.URL.revokeObjectURL(url);
      })
      .catch(error => console.error("请求失败:", error));
  });
});
