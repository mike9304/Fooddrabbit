# Line anEater

## Setup


### 套件

* for pipenv
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* for visualizing Finite State Machine
```sh
pipenv install transitions

pipenv install graphviz
```


* for crawler
```sh
pipenv install beautifulsoup4
```
### Secret Data
You should generate a `.env` file to set Environment Variables.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

### Run the sever

```sh
python3 app.py
```

## Finite State Machine
![fsm](./fsm.png)

### state 說明
* `user`：輸入aneater，開始使用
* `choose_area`：選擇一個區域
* `choose_region`：選擇一個城市
* `choose_restaurant`：選擇推薦餐廳
* `recommand_restaurant`：選擇前往訂餐，或是快速瀏覽菜單
* `recommand_menu`：顯示餐廳菜單

## 使用範例
![1](https://user-images.githubusercontent.com/57171538/147869251-cd8634ed-cd3c-497d-b88e-716f89fc1fcd.png)
![2](https://user-images.githubusercontent.com/57171538/147869252-d20c21a2-0e21-4f14-a729-b024d31893ed.png)
![3](https://user-images.githubusercontent.com/57171538/147869253-08768aa0-4e1e-4ee4-bcc6-8b9b57df4133.png)
![4](https://user-images.githubusercontent.com/57171538/147869254-f2b7c684-76df-420f-a3b5-9433f71ee237.png)
![5](https://user-images.githubusercontent.com/57171538/147869256-e44daa15-04ee-4bc1-b0c3-d34346e69519.png)
![6](https://user-images.githubusercontent.com/57171538/147869257-8b5c7af4-93af-4384-b960-e91bb3fc684b.png)
![7](https://user-images.githubusercontent.com/57171538/147869259-f419550d-d596-4135-9b7c-4328d2189a3e.png)
![8](https://user-images.githubusercontent.com/57171538/147869260-a3b1f249-3f69-47f9-8856-ab602705cb7e.png)

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)



### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

