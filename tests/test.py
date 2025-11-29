import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.search_tools import (
    search_company_overview,
    search_company_shareholders,
    search_company_officers,
    search_company_subsidaries,
    search_company_historical_price,
)
from src.tools.math_tools import (
    calculating_simple_moving_average,
    calculating_relative_strength_index,
    calculating_moving_average_convergence_divergence
)
from src.agent.agent import setup_agent


def test_search_tools():
    """Test all search tools"""
    print("\n" + "="*60)
    print("🔍 Testing Search Tools")
    print("="*60)
    
    ticker = "VCB"  # Vietcombank
    
    try:
        print(f"\n1️⃣ Testing search_company_overview({ticker})...")
        result = search_company_overview.invoke({"ticker": ticker})
        print(f"✅ Success: {result[:100]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    try:
        print(f"\n2️⃣ Testing search_company_shareholders({ticker})...")
        result = search_company_shareholders.invoke({"ticker": ticker})
        print(f"✅ Success: {result[:100]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    try:
        print(f"\n3️⃣ Testing search_company_officers({ticker})...")
        result = search_company_officers.invoke({"ticker": ticker})
        print(f"✅ Success: {result[:100]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    try:
        print(f"\n4️⃣ Testing search_company_subsidaries({ticker})...")
        result = search_company_subsidaries.invoke({"ticker": ticker})
        print(f"✅ Success: {result[:100]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    try:
        print(f"\n5️⃣ Testing search_company_historical_price({ticker})...")
        result = search_company_historical_price.invoke({
            "ticker": ticker,
            "start_day": "2024-01-01",
            "end_day": "2024-01-31",
            "interval": "1d"
        })
        print(f"✅ Success: {result[:100]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_math_tools():
    """Test math tools with sample data"""
    print("\n" + "="*60)
    print("📊 Testing Math Tools")
    print("="*60)
    
    # Sample historical price data
    sample_data = """
    time          open    high     low   close   volume
    2024-01-01   100.0   102.0   99.5   101.5   1000000
    2024-01-02   101.5   103.0  100.0   102.0   1100000
    2024-01-03   102.0   105.0  101.5   104.5   1200000
    2024-01-04   104.5   106.0  103.0   105.0   1300000
    2024-01-05   105.0   107.0  104.0   106.5   1400000
    """
    
    try:
        print("\n1️⃣ Testing calculating_simple_moving_average...")
        result = calculating_simple_moving_average.invoke({
            "data": sample_data,
            "SMA_window": 3
        })
        print(f"✅ Success: {result[:100]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    try:
        print("\n2️⃣ Testing calculating_relative_strength_index...")
        result = calculating_relative_strength_index.invoke({
            "data": sample_data,
            "RSI_window": 3
        })
        print(f"✅ Success: {result[:100]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    try:
        print("\n3️⃣ Testing calculating_moving_average_convergence_divergence...")
        result = calculating_moving_average_convergence_divergence.invoke({
            "data": sample_data,
            "short_span": 2,
            "long_span": 3,
            "signal_span": 2
        })
        print(f"✅ Success: {result[:100]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_agent_creation():
    """Test agent creation"""
    print("\n" + "="*60)
    print("🤖 Testing Agent Creation")
    print("="*60)
    
    try:
        print("\n1️⃣ Creating agent...")
        agent = setup_agent()
        print(f"✅ Agent created successfully: {type(agent)}")
        
        # Check if agent has tools
        if hasattr(agent, 'tools'):
            print(f"✅ Agent has {len(agent.tools)} tools")
        
        return agent
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def test_agent_invoke(agent):
    """Test agent invocation"""
    print("\n" + "="*60)
    print("💬 Testing Agent Invocation")
    print("="*60)
    
    if agent is None:
        print("⚠️ Agent not created, skipping test")
        return
    
    try:
        print("\n1️⃣ Testing agent with question: 'VCB là gì?'")
        result = agent.invoke({
            "messages": [{"role": "user", "content": "VCB là gì?"}]
        })
        
        if result:
            print(f"✅ Agent response received")
            messages = result.get("messages", [])
            
            # Print last message
            if messages:
                last_msg = messages[-1]
                print(f"Last message type: {last_msg.__class__.__name__}")
                if hasattr(last_msg, 'content'):
                    print(f"Content: {last_msg.content[:200]}...")
        else:
            print("⚠️ No response from agent")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_api():
    """Test API endpoint"""
    print("\n" + "="*60)
    print("🌐 Testing API Endpoint")
    print("="*60)
    
    try:
        import requests
        
        print("\n1️⃣ Testing API at http://localhost:8000/ask")
        
        response = requests.post(
            "http://localhost:8000/ask",
            json={"question": "VCB là gì?"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response received (Status: {response.status_code})")
            print(f"Question: {data.get('user_question')}")
            print(f"Tools used: {data.get('tool_used')}")
            print(f"Answer: {str(data.get('answer'))[:100]}...")
        else:
            print(f"❌ API Error (Status: {response.status_code})")
            print(f"Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API at http://localhost:8000")
        print("💡 Make sure FastAPI server is running:")
        print("   python -m uvicorn src.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 FINANCE AI AGENT - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    # Test search tools
    test_search_tools()
    
    # Test math tools
    test_math_tools()
    
    # Test agent creation
    agent = test_agent_creation()
    
    # Test agent invocation
    test_agent_invoke(agent)
    
    # Test API
    test_api()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    main()