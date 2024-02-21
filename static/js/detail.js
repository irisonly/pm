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

function handle_delete(event) {
  const query_string = window.location.search;
  const query_url = new URLSearchParams(query_string);
  const id = { id: query_url.get("id") };
  console.log(event, id);
  fetch(END_POINT + "/project", {
    method: "DELETE", // 指定请求方法为 POST
    headers: {
      // 指定发送的数据类型为 JSON
      "Content-Type": "application/json",
    },
    body: JSON.stringify(id), // 将 JavaScript 对象转换为 JSON 字符串
  })
    .then(response => response.json()) // 解析 JSON 响应
    .then(data => {
      console.log("Success:", id);
      // alert("项目已经删除");
      window.location.href = "./index.html";
    })
    .catch(error => {
      console.error("Error:", error);
      alert("项目删除失败，请检查");
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

const promise_type = fetch(END_POINT + "/type", {
  method: "GET",
  headers: { Authorization: "Bearer " + get_token() },
})
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    type_select(data, "type_id");
  })
  .catch(error => console.error("请求失败:", error));

const promise_status = fetch(END_POINT + "/status")
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    type_select(data, "status_id");
  })
  .catch(error => console.error("请求失败:", error));

Promise.all([promise_charge, promise_status, promise_type])
  .then(response => {})
  .then(data => {
    const query_string = window.location.search;
    const query_url = new URLSearchParams(query_string);
    const id = query_url.get("id");

    fetch(
      END_POINT + "/project?name&charge_p_id&type_id&charge_m_id&id=" + id,
      {
        method: "GET",
        headers: { Authorization: "Bearer " + get_token() },
      }
    )
      .then(response => response.json()) // 将响应转换为JSON
      .then(data => {
        // console.log(data);
        const original_data = data["response"];
        console.log(original_data);
        document.getElementById("name").value = original_data.name;
        document.getElementById("payment").value = original_data.payment;
        document.getElementById("cost").value = original_data.cost;
        document.getElementById("balance_payment").value =
          original_data.balance_payment;
        document.getElementById("start_time").value = original_data.start_time;
        document.getElementById("end_time").value = original_data.end_time;
        select_default("type_id", original_data.type_id);
        select_default("status_id", original_data.status_id);
        const m_list = [];
        original_data.m_charges.forEach(element => {
          m_list.unshift(element.id);
        });
        const p_list = [];
        original_data.p_charges.forEach(element => {
          p_list.unshift(element.id);
        });
        console.log(m_list, p_list);
        const m = document.getElementsByName("m");
        m.forEach(element => {
          console.log(parseInt(element.value, 10));
          if (m_list.includes(parseInt(element.value, 10))) {
            element.checked = true;
          }
        });
        const p = document.getElementsByName("p");
        p.forEach(element => {
          if (p_list.includes(parseInt(element.value, 10))) {
            element.checked = true;
          }
        });
      })
      .catch(error => {
        console.error("请求失败:", error);
        window.location.href = "./login.html";
      });
  });

document.addEventListener("DOMContentLoaded", () => {
  const query_string = window.location.search;
  const query_url = new URLSearchParams(query_string);
  const id = query_url.get("id");

  const form = document.getElementById("project_form");

  form.addEventListener("submit", e => {
    e.preventDefault();
    const form_data = new FormData(form);
    const form_api = {};
    form_data.forEach((value, key) => {
      form_api[key] = value;
    });
    form_api["id"] = parseInt(id, 10);
    form_api["type_id"] = parseInt(form_api["type_id"], 10);
    form_api["charge_id"] = parseInt(form_api["charge_id"], 10);
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
        window.location.href = "./index.html";
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
