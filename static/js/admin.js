import { END_POINT, super_admin } from "./config.js";
let select_d = [];

function get_token() {
  // console.log(localStorage.getItem("access_token"));
  return localStorage.getItem("access_token");
}

const promise_charge = fetch(END_POINT + "/projectlist?id=0", {
  method: "GET",
  headers: { Authorization: "Bearer " + get_token() },
})
  .then(response => response.json()) // 将响应转换为JSON
  .then(data => {
    const charge_select = document.getElementById("project_admin");
    data.response.forEach(element => {
      const opt = document.createElement("input");
      opt.type = "checkbox";
      opt.name = "m";
      opt.value = element.id;

      charge_select.appendChild(opt);
      if (select_d.includes(element.id)) {
        opt.checked = true;
      }
      const label = document.createElement("label");
      label.textContent = element.name;
      charge_select.appendChild(label);
    });
  })
  .catch(error => console.error("请求失败:", error));
const query_string = window.location.search;
const query_url = new URLSearchParams(query_string);
const id = query_url.get("id");
const project_selected = fetch(END_POINT + "/adminproject?id=" + id, {
  method: "GET",
})
  .then(response => response.json())
  .then(data => {
    console.log(data);
    select_d = data.response.map(ele => {
      console.log(ele);
      return ele.id;
    });
    console.log(select_d);
  });

Promise.all([project_selected, promise_charge])
  .then(response => {})
  .then(data => {});

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

    var checkboxes = document.getElementsByName("m");
    var selectedm = [];

    // 遍历多选框，检查是否被选中
    for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].checked) {
        // 如果选中，将其value添加到selectedFruits数组中
        selectedm.push(parseInt(checkboxes[i].value, 10));
      }
    }
    form_api["admin_id"] = parseInt(id, 10);

    form_api["project_list"] = selectedm;
    console.log(form_api);
    fetch(END_POINT + "/adminproject", {
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
        alert("修改成功");
        window.location.href = "./index.html";
      })
      .catch(error => {
        console.error("Error:", error);
        alert("修改失败，请检查");
      });
  });

  // 使用 fetch 发起 POST 请求
});
