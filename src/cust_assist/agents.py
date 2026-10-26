from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase, agent, task, crew
from src.cust_assist.tools.calculate_warranty_status import WarrantyStatusTool
from src.cust_assist.tools.check_order_delivery import OrderDeliveryTool
from src.cust_assist.tools.create_warranty_claim import CreateClaimTool
from src.cust_assist.tools.find_all_purchases import CustomerPurchasesTool
from src.cust_assist.tools.find_customer import FindCustomerTool
from src.cust_assist.tools.show_claim_history import ClaimHistoryTool
from src.cust_assist.tools.show_product_details import ProductDetailsTool
from src.cust_assist.tools.track_claim_status import ClaimStatusTool
from src.cust_assist.tools.verify_serial_number import VerifySerialTool
from src.cust_assist.tools.damage_inspection import DamageInspectionTool
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
load_dotenv()

class InputFields(BaseModel):
    email : EmailStr
    phone : str
    serial_number : str
    product_name : str
    ticket_id  : str
    customer_id : int
    customer_name : str
    issue_summary : str

@CrewBase
class Warranty:

    agents_config="config/agents.yaml"
    tasks_config="config/tasks.yaml"

    def __init__(self):

        self.llm= LLM(
                            model="ollama/maternion/minicpm5:2b",
                            base_url="http://localhost:11434"
                        )
        
        self.warranty_status_tool = WarrantyStatusTool()
        self.order_delivery_tool = OrderDeliveryTool()
        self.create_claim_tool = CreateClaimTool()
        self.customer_purchase_tool = CustomerPurchasesTool()
        self.find_customer_tool = FindCustomerTool()
        self.claim_history_tool = ClaimHistoryTool()
        self.product_details_tool = ProductDetailsTool()
        self.claim_status_tool = ClaimStatusTool()
        self.verify_serial_tool = VerifySerialTool()
        
    @agent
    def intake_agent(self):
        return Agent(
            config=self.agents_config['intake_agent'],
            llm=self.llm,
            verbose=True
        )
        
    @agent
    def validation_agent(self):
        return Agent(
            config=self.agents_config['validation_agent'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def damage_inspection_agent(self):
        return Agent(
            config=self.agents_config['damage_inspection_agent'],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def claim_agent(self):
        return Agent(
            config=self.agents_config['claim_agent'],
            llm=self.llm,
            verbose= True

        )

    @agent
    def resolution_agent(self):
        return Agent(
            config=self.agents_config['resolution_agent'],
            llm=self.llm,
            verbose= True
        )

    @agent
    def communication_agent(self):
        return Agent(
            config=self.agents_config['communication_agent'],
            llm=self.llm,
            verbose= True
        )

    
    @task
    def intake_task(self):
        return Task(
            config=self.tasks_config["intake_task"],
            tools=[
                self.find_customer_tool, 
                self.customer_purchase_tool,
                self.verify_serial_tool
                    ],
            output_pydantic=InputFields,
            verbose=True,

        )

    @task
    def validation_task(self):
        return Task(
            config=self.tasks_config['validation_task'],
            verbose=True,
            tools=[
                self.verify_serial_tool,
                self.warranty_status_tool,
                self.order_delivery_tool
            ]
        )


    @task
    def damage_inspection_task(self):
            return Task(
                config=self.tasks_config['damage_inspection_task'],
                tools=[DamageInspectionTool()],
                verbose= True
            )


    
    @task
    def claim_task(self):
        return Task(
            config=self.tasks_config['claim_task'],
            tools=[
                self.create_claim_tool,
                self.claim_status_tool,
                self.claim_history_tool

            ],
            verbose= True
        )

    @task
    def resolution_task(self):
        return Task(
            config=self.tasks_config['resolution_task'],
            verbose= True,

        )
    @task
    def communication_task(self):
        return Task(
            config=self.tasks_config['communication_task'],
            verbose= True
        )

    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )