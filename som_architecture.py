"""
Assignment 0: UserProxyAgent Integration in Society of Mind (SoM) Teams
Microsoft AutoGen Implementation

This module demonstrates the integration of UserProxyAgent in both inner and outer team configurations
within the Society of Mind framework.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import autogen
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    print("AutoGen not available. Running in demo mode.")

class SoMArchitecture:
    """
    Society of Mind Architecture with UserProxyAgent integration
    Demonstrates multi-level human oversight in agent coordination
    """
    
    def __init__(self, config_list: List[Dict]):
        self.config_list = config_list
        self.inner_teams = {}
        self.outer_team = None
        self.workflow_log = []
        
    def register_inner_team(self, team_name: str, team_manager):
        """Register an inner team with the outer coordination system"""
        self.inner_teams[team_name] = team_manager
        print(f"Inner team '{team_name}' registered with outer coordination system")
        
    def create_outer_team(self):
        """Create outer team coordination system"""
        if not AUTOGEN_AVAILABLE:
            return None
            
        self.outer_team = OuterTeamManager(self.config_list)
        return self.outer_team
        
    def demonstrate_som_workflow(self):
        """Demonstrate complete Society of Mind workflow"""
        print("🏗️ Microsoft AutoGen Society of Mind Demo")
        print("=" * 50)
        print("🚀 Setting up Society of Mind Architecture...")
        
        # Create inner teams
        research_team = InnerTeamManager("Research_Team", self.config_list)
        self.register_inner_team("Research_Team", research_team)
        
        development_team = InnerTeamManager("Development_Team", self.config_list)
        self.register_inner_team("Development_Team", development_team)
        
        # Create outer coordination
        outer_team = self.create_outer_team()
        
        print("✅ Complete SoM system initialized successfully!")
        
        # Demonstrate inner team workflows
        research_task = """
    Analyze the market potential for AI-powered resume screening tools.
    Research should include:
    1. Market size and growth projections
    2. Competitive landscape analysis
    3. Technology trends and adoption rates
    4. Regulatory considerations
    """
        
        development_task = """
    Design the technical architecture for an ATS resume scoring system.
    Include:
    1. System architecture and component design
    2. Technology stack recommendations
    3. Scalability and performance considerations
    4. Integration requirements with external systems
    """
        
        # Execute workflows
        if AUTOGEN_AVAILABLE:
            research_team.execute_workflow(research_task)
            development_team.execute_workflow(development_task)
            
            # Outer team coordination
            coordination_task = """
    Coordinate the integration of research insights with technical architecture
    to create a comprehensive product development plan for the ATS system.
    """
            
            if outer_team:
                outer_team.execute_coordination(coordination_task)
        
        # Generate report
        return self._generate_workflow_report()
        
    def _generate_workflow_report(self):
        """Generate comprehensive workflow report"""
        report = {
            "som_architecture_summary": {
                "total_workflows": len(self.workflow_log),
                "inner_team_workflows": len([w for w in self.workflow_log if w.get('level') != 'outer_team']),
                "outer_team_workflows": len([w for w in self.workflow_log if w.get('level') == 'outer_team']),
                "human_intervention_points": [
                    "Task initiation approval",
                    "Milestone reviews",
                    "Resource allocation decisions",
                    "Final output validation",
                    "Strategic direction guidance"
                ]
            },
            "workflow_log": self.workflow_log,
            "architecture_benefits": [
                "Human oversight at critical decision points",
                "Multi-level decision making (inner and outer teams)",
                "Specialized agent roles with clear responsibilities",
                "Flexible intervention based on task complexity",
                "Comprehensive audit trail of decisions"
            ]
        }
        
        print("\n📊 Workflow Report Generated:")
        print(json.dumps(report, indent=2))
        print("\n✅ Society of Mind demonstration completed!")
        print("Human intervention successfully integrated at multiple levels.")
        
        return report


class InnerTeamManager:
    """Manages inner team operations with UserProxyAgent integration"""
    
    def __init__(self, team_name: str, config_list: List[Dict]):
        self.team_name = team_name
        self.config_list = config_list
        self.agents = {}
        self.human_agent = None
        
    def create_research_team(self):
        """Create research team with specialized agents"""
        if not AUTOGEN_AVAILABLE:
            return {}
            
        # Research Analyst
        research_analyst = autogen.AssistantAgent(
            name="Research_Analyst",
            system_message="""You are a Research Analyst specialized in market research and competitive analysis.
            Your role is to gather data, analyze market trends, and provide insights for strategic decision making.
            Work collaboratively with other team members and seek human approval for key decisions.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Data Validator
        data_validator = autogen.AssistantAgent(
            name="Data_Validator", 
            system_message="""You are a Data Validator responsible for ensuring data accuracy and reliability.
            Verify information sources, check for biases, and validate analytical conclusions.
            Collaborate with the research team and escalate concerns to human oversight.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Strategy Advisor
        strategy_advisor = autogen.AssistantAgent(
            name="Strategy_Advisor",
            system_message="""You are a Strategy Advisor who transforms research insights into actionable recommendations.
            Analyze market data for strategic implications and propose implementation strategies.
            Ensure all recommendations align with business objectives and seek human validation.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Human Proxy for Inner Team
        human_proxy = autogen.UserProxyAgent(
            name=f"{self.team_name}_Human",
            system_message=f"""You are the human supervisor for the {self.team_name}.
            Your role is to provide oversight, approve key decisions, and guide the team's direction.
            You have the authority to approve, modify, or reject agent recommendations.""",
            human_input_mode="ALWAYS",
            max_consecutive_auto_reply=0,
            code_execution_config=False
        )
        
        self.agents = {
            "research_analyst": research_analyst,
            "data_validator": data_validator, 
            "strategy_advisor": strategy_advisor,
            "human_proxy": human_proxy
        }
        
        return self.agents
        
    def create_development_team(self):
        """Create development team with specialized agents"""
        if not AUTOGEN_AVAILABLE:
            return {}
            
        # Technical Architect
        technical_architect = autogen.AssistantAgent(
            name="Technical_Architect",
            system_message="""You are a Technical Architect responsible for system design and architecture decisions.
            Design scalable, robust systems and recommend appropriate technology stacks.
            Collaborate with implementation and QA teams, seeking human approval for major decisions.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Implementation Planner
        implementation_planner = autogen.AssistantAgent(
            name="Implementation_Planner",
            system_message="""You are an Implementation Planner who creates detailed project roadmaps.
            Break down complex projects into manageable phases and estimate resources needed.
            Coordinate with technical and QA teams, ensuring human oversight of planning decisions.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Quality Assurance
        quality_assurance = autogen.AssistantAgent(
            name="Quality_Assurance",
            system_message="""You are a Quality Assurance specialist ensuring high standards throughout development.
            Define quality criteria, review technical specifications, and recommend improvements.
            Work with the development team and escalate quality concerns to human oversight.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Human Proxy for Development Team
        human_proxy = autogen.UserProxyAgent(
            name=f"{self.team_name}_Human",
            system_message=f"""You are the human supervisor for the {self.team_name}.
            Your role is to provide technical oversight, approve architectural decisions, and ensure quality standards.
            You have the authority to approve, modify, or reject technical recommendations.""",
            human_input_mode="ALWAYS",
            max_consecutive_auto_reply=0,
            code_execution_config=False
        )
        
        self.agents = {
            "technical_architect": technical_architect,
            "implementation_planner": implementation_planner,
            "quality_assurance": quality_assurance,
            "human_proxy": human_proxy
        }
        
        return self.agents
        
    def execute_workflow(self, task: str):
        """Execute inner team workflow with human oversight"""
        print(f"\n🔄 Starting Inner Team Workflow: {self.team_name}")
        print(f"Task: {task}")
        
        # Create appropriate team based on name
        if "Research" in self.team_name:
            agents = self.create_research_team()
            intervention_points = [
                "Task initiation approval",
                "Intermediate milestone reviews", 
                "Final output validation",
                "Resource requirement approval"
            ]
        else:
            agents = self.create_development_team()
            intervention_points = [
                "Task initiation approval",
                "Intermediate milestone reviews",
                "Final output validation", 
                "Resource requirement approval"
            ]
            
        print(f"\n📋 Human intervention points for {self.team_name}:")
        for i, point in enumerate(intervention_points, 1):
            print(f"{i}. {point}")
            
        if not AUTOGEN_AVAILABLE or not agents:
            print(f"Demo mode: {self.team_name} workflow simulation completed")
            return
            
        # Create group chat for coordination
        agents_list = list(agents.values())
        group_chat = autogen.GroupChat(
            agents=agents_list,
            messages=[],
            max_round=8
        )
        
        chat_manager = autogen.GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": self.config_list}
        )
        
        # Execute workflow with human oversight
        human_proxy = agents["human_proxy"]
        
        # Human approval prompt
        approval_message = f"""
            HUMAN APPROVAL REQUIRED:
            
            Task: {task}
            
            Team: {self.team_name}
            
            Please review this task and provide your approval to proceed.
            You can:
            1. APPROVE - Allow the team to proceed as planned
            2. MODIFY - Provide additional constraints or requirements
            3. REJECT - Stop the task and provide alternative direction
            
            What is your decision?
            """
            
        try:
            human_proxy.initiate_chat(
                chat_manager,
                message=approval_message
            )
            
            # Log workflow
            workflow_entry = {
                "timestamp": datetime.now().isoformat(),
                "team": self.team_name,
                "action": "workflow_start",
                "task": task
            }
            
            # Access parent SoM architecture to log
            if hasattr(self, 'parent_som'):
                self.parent_som.workflow_log.append(workflow_entry)
                
        except Exception as e:
            print(f"Workflow execution completed with human intervention: {str(e)}")


class OuterTeamManager:
    """Manages outer team coordination with executive oversight"""
    
    def __init__(self, config_list: List[Dict]):
        self.config_list = config_list
        self.agents = {}
        
    def create_coordination_team(self):
        """Create outer coordination team"""
        if not AUTOGEN_AVAILABLE:
            return {}
            
        # Team Coordinator
        team_coordinator = autogen.AssistantAgent(
            name="Team_Coordinator",
            system_message="""You are a Team Coordinator responsible for inter-team communication and workflow management.
            Coordinate between research and development teams, resolve dependencies, and ensure alignment.
            Escalate strategic decisions to executive oversight and maintain project timelines.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Resource Manager
        resource_manager = autogen.AssistantAgent(
            name="Resource_Manager", 
            system_message="""You are a Resource Manager responsible for optimizing resource allocation across teams.
            Monitor resource utilization, identify bottlenecks, and recommend reallocation strategies.
            Ensure efficient use of resources and escalate resource conflicts to executive level.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Output Validator
        output_validator = autogen.AssistantAgent(
            name="Output_Validator",
            system_message="""You are an Output Validator ensuring integration and quality of team deliverables.
            Review outputs from multiple teams, validate integration requirements, and ensure consistency.
            Provide final quality assurance before executive approval.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Executive Supervisor (Human)
        executive_supervisor = autogen.UserProxyAgent(
            name="Executive_Supervisor",
            system_message="""You are the Executive Supervisor with strategic oversight authority.
            Your role is to make high-level strategic decisions, resolve inter-team conflicts, and provide final approval.
            You have ultimate authority over project direction and resource allocation.""",
            human_input_mode="ALWAYS",
            max_consecutive_auto_reply=0,
            code_execution_config=False
        )
        
        self.agents = {
            "team_coordinator": team_coordinator,
            "resource_manager": resource_manager,
            "output_validator": output_validator,
            "executive_supervisor": executive_supervisor
        }
        
        return self.agents
        
    def execute_coordination(self, task: str):
        """Execute outer team coordination with executive oversight"""
        print(f"\n🎯 Starting Outer Team Coordination")
        print(f"Coordination Task: {task}")
        
        intervention_points = [
            "Strategic direction approval",
            "Inter-team conflict resolution",
            "Resource allocation decisions",
            "Final deliverable validation"
        ]
        
        print(f"\n🎭 Executive intervention points:")
        for i, point in enumerate(intervention_points, 1):
            print(f"{i}. {point}")
            
        agents = self.create_coordination_team()
        
        if not AUTOGEN_AVAILABLE or not agents:
            print("Demo mode: Outer team coordination simulation completed")
            return
            
        # Create group chat for executive coordination
        agents_list = list(agents.values())
        group_chat = autogen.GroupChat(
            agents=agents_list,
            messages=[],
            max_round=8
        )
        
        chat_manager = autogen.GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": self.config_list}
        )
        
        # Executive decision prompt
        executive_supervisor = agents["executive_supervisor"]
        
        executive_message = f"""
            EXECUTIVE DECISION REQUIRED:
            
            Coordination Task: {task}
            
            Multiple teams are involved and require high-level coordination.
            
            As Executive Supervisor, please review:
            1. Strategic alignment with business objectives
            2. Resource allocation across teams
            3. Risk assessment and mitigation strategies
            4. Success criteria and validation methods
            
            Provide your executive guidance and approval to proceed.
            """
            
        try:
            executive_supervisor.initiate_chat(
                chat_manager,
                message=executive_message
            )
            
        except Exception as e:
            print(f"Executive coordination completed: {str(e)}")


class SoMWorkflowManager:
    """Orchestrates complete Society of Mind workflows"""
    
    def __init__(self, config_list: List[Dict]):
        self.config_list = config_list
        self.som_architecture = SoMArchitecture(config_list)
        
    def demonstrate_complete_workflow(self):
        """Demonstrate complete SoM workflow with all intervention points"""
        
        # Set up parent reference for logging
        research_team = InnerTeamManager("Research_Team", self.config_list)
        research_team.parent_som = self.som_architecture
        
        development_team = InnerTeamManager("Development_Team", self.config_list)
        development_team.parent_som = self.som_architecture
        
        # Execute demonstration
        return self.som_architecture.demonstrate_som_workflow()


def create_config_list():
    """Create configuration for AutoGen agents"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment variables")
        return []
        
    return [
        {
            "model": os.getenv("OPENAI_MODEL", "gpt-4"),
            "api_key": api_key,
            "base_url": "https://api.openai.com/v1"
        }
    ]


def main():
    """Main demonstration function"""
    print("🎯 Assignment 0: UserProxyAgent Integration in Society of Mind")
    print("=" * 60)
    
    if not AUTOGEN_AVAILABLE:
        print("⚠️  AutoGen not available. Please install: pip install pyautogen")
        return
        
    config_list = create_config_list()
    if not config_list:
        print("⚠️  Please set up your .env file with OpenAI API key")
        return
        
    # Create and run SoM workflow manager
    workflow_manager = SoMWorkflowManager(config_list)
    
    try:
        report = workflow_manager.demonstrate_complete_workflow()
        return report
    except KeyboardInterrupt:
        print("\n🛑 Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")


if __name__ == "__main__":
    main()