import { END_POINT } from "./config.js";

function type_select(data, _id) {
  const response = data.response;
  console.log(response);
  const select_form = document.getElementById(_id);
  response.forEach(element => {
    const opt = document.createElement("option");
    opt.value = element.id;
    opt.textContent = element.name;
    select_form.appendChild(opt);
  });
}

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

function select_default(select_id, default_value) {
  const select = document.getElementById(select_id);
  const sel = select.options;
  Array.from(sel).forEach((ele, ind) => {
    if (parseInt(ele.value, 10) == default_value) {
      select.selectedIndex = ind;
    }
  });
}

const promise_charge = fetch(END_POINT + "/charge")
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    const charge_select = document.getElementById("charge_m");
    data.response.forEach(element => {
      const opt = document.createElement("input");
      opt.type = "checkbox";
      opt.name = "m";
      opt.value = element.id;
      charge_select.appendChild(opt);
      const label = document.createElement("label");
      label.textContent = element.name;
      charge_select.appendChild(label);
    });
    const charge_p_select = document.getElementById("charge_p");
    data.response.forEach(element => {
      const opt = document.createElement("input");
      opt.type = "checkbox";
      opt.name = "p";
      opt.value = element.id;
      charge_p_select.appendChild(opt);
      const label = document.createElement("label");
      label.textContent = element.name;
      charge_p_select.appendChild(label);
    });
  })
  .catch(error => console.error("请求失败:", error));

const promise_type = fetch(END_POINT + "/type?name=", {
  method: "GET",
  headers: { Authorization: "Bearer " + get_token() },
})
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    type_select(data, "type_id");
  })
  .catch(error => {
    console.error("请求失败:", error);
    window.location.href = "./login.html";
  });

const promise_status = fetch(END_POINT + "/status?name=")
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    type_select(data, "status_id");
  })
  .catch(error => console.error("请求失败:", error));

Promise.all([promise_charge, promise_status, promise_type])
  .then(response => {})
  .then(data => {});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("project_form");

  form.addEventListener("submit", e => {
    e.preventDefault();
    const form_data = new FormData(form);
    const form_api = {};
    form_data.forEach((value, key) => {
      form_api[key] = value;
    });
    form_api["type_id"] = parseInt(form_api["type_id"], 10);
    form_api["status_id"] = parseInt(form_api["status_id"], 10);
    form_api["balance_payment"] = parseInt(form_api["balance_payment"], 10);
    form_api["payment"] = parseInt(form_api["payment"], 10);
    form_api["cost"] = parseInt(form_api["cost"], 10);
    var checkboxes = document.getElementsByName("m");
    var selectedm = [];

    // 遍历多选框，检查是否被选中
    for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].checked) {
        // 如果选中，将其value添加到selectedFruits数组中
        selectedm.push(parseInt(checkboxes[i].value, 10));
      }
    }
    var checkboxes = document.getElementsByName("p");
    var selectedp = [];

    // 遍历多选框，检查是否被选中
    for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].checked) {
        // 如果选中，将其value添加到selectedFruits数组中
        selectedp.push(parseInt(checkboxes[i].value, 10));
      }
    }
    form_api["m_id_list"] = selectedm;
    form_api["p_id_list"] = selectedp;
    console.log(form_api);
    fetch(END_POINT + "/project", {
      method: "POST", // 指定请求方法为 POST
      headers: {
        // 指定发送的数据类型为 JSON
        "Content-Type": "application/json",
        Authorization: "Bearer " + get_token(),
      },
      body: JSON.stringify(form_api), // 将 JavaScript 对象转换为 JSON 字符串
    })
      .then(response => response.json()) // 解析 JSON 响应
      .then(data => {
        console.log("Success:", form_api);
        window.location.href = "./index.html";
      })
      .catch(error => {
        console.error("Error:", error);
        alert("项目创建失败，请检查");
      });
  });

  // 使用 fetch 发起 POST 请求
});
