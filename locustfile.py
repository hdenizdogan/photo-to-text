from locust import HttpUser,task
import locust

class Testing(HttpUser):
    @task
    def send_photo(self):
        self.client.get(url="/send/?remote_url=https://www.ssk.biz.tr/wp-content/uploads/2016/09/ziraat-bankasi-hesap-no-bulma.jpg")