from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib.parse import quote  # 中文錯誤網址進行編碼

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"))
templates = Jinja2Templates(directory="templates")

# 假設帳號和密碼存儲在數據庫中
fake_username = "test"
fake_password = "test"

# 登入頁面
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 登入驗證端點
@app.post("/signin")
async def login(request: Request, username: str = Form(...), password: str = Form(...), agree: bool = Form(...)):
    # 這裡可以添加身份驗證邏輯，然後根據驗證結果進行相應的操作
    if username == fake_username and password == fake_password and agree:
        return RedirectResponse(url="/member")  # 登入成功，重定向到 成功路徑
    else:
        error_message = "帳號或密碼錯誤"
        return RedirectResponse(url=f"/error?message={error_message}") # 登入失敗，重定向回登入頁面並顯示錯誤消息

# 登入成功頁面
@app.post("/member", response_class=HTMLResponse)
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


# 登出端點
@app.get("/signout")
async def signout(request: Request):
     # 清除帳號和密碼
     # 設置為空值的操作
    username = ""
    password = ""
    return RedirectResponse(url="/")


# 登入失敗頁面
@app.post("/error", response_class=HTMLResponse)
async def error_page(request: Request, message: str = None):
    return templates.TemplateResponse("failure.html", {"request": request, "message": message})

@app.get("/error", response_class=HTMLResponse)
async def redirect_to_home(request: Request):
    # 清除帳號和密碼
    # 設置為空值的操作
    username = ""
    password = ""
    return RedirectResponse(url="/")   # 將用戶重定向到首頁

