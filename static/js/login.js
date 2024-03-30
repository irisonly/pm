import { END_POINT } from "./config.js";

document.addEventListener("DOMContentLoaded", () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  const form = document.getElementById("project_form");
  form.addEventListener("submit", e => {
    e.preventDefault();
    const form_data = new FormData(form);
    const form_api = {};
    form_data.forEach((value, key) => {
      form_api[key] = value;
    });
    console.log(form_api);
    fetch(END_POINT + "/login", {
      method: "POST", // 指定请求方法为 POST
      headers: {
        // 指定发送的数据类型为 JSON
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form_api), // 将 JavaScript 对象转换为 JSON 字符串
    })
      .then(response => response.json()) // 解析 JSON 响应
      .then(data => {
        if (data["response"] == "error") {
          alert("用户名或密码错误");
        } else {
          localStorage.setItem(
            "access_token",
            data["response"]["access_token"]
          );
          localStorage.setItem(
            "refresh_token",
            data["response"]["refresh_token"]
          );
          localStorage.setItem("id", data["response"]["id"]);
          window.location.href = "./index.html";
        }
      })
      .catch(error => {
        console.error("Error:", error);
        alert("登录失败，请重试");
      });
  });
});
