from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from scrapper.models import Answer, Questionary, Question, QuestionAnswers
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse, Request

class TodoTestSpyder(scrapy.Spider):
    name = 'todotest_spyder'
    start_urls = ["http://www.todotest.com/tests/test_motocicleta_idx.asp?t=6"]

    mike_cookies = {
        "TodoTest" : "ta=1&hu=984347c8551ebf2789129f29a805a362&nu=4191619"
    }

    def __init__(self):
        super(TodoTestSpyder, self).__init__(name=self.name)
        self.scrappin_app = ScrappingApp()

    def make_requests_from_url(self, url):
        request = super(TodoTestSpyder, self).make_requests_from_url(url)
        # We need a cookie session from a valid logged user
        request.cookies['TodoTest'] = self.mike_cookies["TodoTest"]
        return request

    def parse(self, response):
        links = Selector(response=response).xpath("//table[@class='tbl_idxtests']//td[@class='cap_fil']/a/@href")
        for href in links:
            full_link = "http://www.todotest.com/tests/" + href.extract()
            yield scrapy.Request(
                full_link,
                callback=self.parse_questionary
            )

    def parse_questionary(self, response):
        # Read all the answers id and do a post with them

        # First input element of each question
        answers = Selector(response=response).xpath("//div[@class='preg']//div[@class='resp'][1]/input")

        input_data = {}
        for answer in answers:
            input_data[answer.xpath("@name").extract()[0]] = answer.xpath("@value").extract()[0]

        return scrapy.FormRequest(
            response.url,
            callback=self.parse_answered_questionary,
            method="POST",
            formdata=input_data
        )

    def parse_answered_questionary(self, response):

        questions = Selector(response=response).xpath("//div[@class='preg']")
        # PARSE AND SAVE QUE FINAL QUESTIONARY
        for question in questions:
            question_text = question.xpath("span[@class='preg_text']").extract()[0]
            answers = question.xpath("div[@class='resp']/div[@class='resp_text']")
            question_answers = [
                answers[0].extract()[0],
                answers[1].extract()[0],
                answers[2].extract()[0],
            ]
            print(question_text, question_answers)




class ScrappingApp(object):

    def __init__(self):
        self.engine = create_engine(
            "postgresql://postgres:mysecretpassword@localhost:32770/driving_tests",
            echo=False
        )

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def scrap_the_hell_out_of_todotest(self): pass


    def create_questionary(self, link):
        questionary = Questionary()
        questionary.todotest_link = link
        self.session.add(questionary)
        self.session.commit()

if __name__ == "__main__":
    sc = ScrappingApp()
    sc.create_questionary("some question,")
