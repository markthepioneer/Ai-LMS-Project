"""
Life Balance AI Service Module

This module provides AI-powered analysis and recommendations for maintaining work-life balance:
- Activity analysis and categorization
- Balance scoring and metrics
- Personalized recommendations
- Stress and burnout detection
- Schedule optimization
"""

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import openai
import numpy as np
from app.utils.logger import get_logger

logger = get_logger(__name__)

class LifeBalanceAI:
    def __init__(self):
        """Initialize the Life Balance AI service."""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key
        
        # Define life domains for balance analysis
        self.LIFE_DOMAINS = [
            'work',
            'health',
            'relationships',
            'personal_growth',
            'recreation',
            'spirituality',
            'community'
        ]
        
        # Activity categories and their domain mappings
        self.ACTIVITY_CATEGORIES = {
            'work': ['meetings', 'emails', 'projects', 'planning'],
            'health': ['exercise', 'meditation', 'sleep', 'nutrition'],
            'relationships': ['family_time', 'social_activities', 'dating', 'communication'],
            'personal_growth': ['learning', 'reading', 'skills', 'hobbies'],
            'recreation': ['entertainment', 'sports', 'travel', 'relaxation'],
            'spirituality': ['meditation', 'reflection', 'worship', 'mindfulness'],
            'community': ['volunteering', 'networking', 'social_causes', 'mentoring']
        }

    async def analyze_balance(self, activities: List[Dict], timeframe: str = 'week') -> Dict:
        """
        Analyze life balance based on activities and provide comprehensive insights.
        
        Args:
            activities: List of activity records with type, duration, and timestamp
            timeframe: Analysis timeframe ('day', 'week', 'month')
            
        Returns:
            Dict containing balance analysis, scores, and recommendations
        """
        try:
            # Calculate domain scores
            domain_scores = self._calculate_domain_scores(activities, timeframe)
            
            # Generate balance insights
            insights = await self._generate_balance_insights(domain_scores, activities)
            
            # Get personalized recommendations
            recommendations = await self.generate_recommendations(domain_scores, activities)
            
            # Calculate overall balance score
            balance_score = self._calculate_overall_score(domain_scores)
            
            # Detect potential burnout risks
            burnout_risk = await self.assess_burnout_risk(activities, domain_scores)
            
            return {
                'balance_score': balance_score,
                'domain_scores': domain_scores,
                'insights': insights,
                'recommendations': recommendations,
                'burnout_risk': burnout_risk,
                'analyzed_at': datetime.utcnow().isoformat(),
                'timeframe': timeframe
            }
        except Exception as e:
            logger.error(f"Error analyzing life balance: {str(e)}")
            raise

    def _calculate_domain_scores(self, activities: List[Dict], timeframe: str) -> Dict[str, float]:
        """Calculate balance scores for each life domain."""
        try:
            # Initialize scores
            domain_scores = {domain: 0.0 for domain in self.LIFE_DOMAINS}
            
            # Calculate total time spent in each domain
            total_time = sum(activity['duration'] for activity in activities)
            domain_times = {domain: 0.0 for domain in self.LIFE_DOMAINS}
            
            for activity in activities:
                # Map activity to domain
                domain = self._map_activity_to_domain(activity['type'])
                if domain:
                    domain_times[domain] += activity['duration']
            
            # Calculate scores based on time distribution
            ideal_distribution = 1.0 / len(self.LIFE_DOMAINS)
            for domain in self.LIFE_DOMAINS:
                if total_time > 0:
                    actual_distribution = domain_times[domain] / total_time
                    # Score based on how close to ideal distribution
                    domain_scores[domain] = 1.0 - min(1.0, abs(actual_distribution - ideal_distribution) / ideal_distribution)
                else:
                    domain_scores[domain] = 0.0
                    
            return domain_scores
        except Exception as e:
            logger.error(f"Error calculating domain scores: {str(e)}")
            return {domain: 0.0 for domain in self.LIFE_DOMAINS}

    def _map_activity_to_domain(self, activity_type: str) -> Optional[str]:
        """Map an activity type to its corresponding life domain."""
        for domain, categories in self.ACTIVITY_CATEGORIES.items():
            if activity_type.lower() in categories:
                return domain
        return None

    def _calculate_overall_score(self, domain_scores: Dict[str, float]) -> float:
        """Calculate overall balance score from domain scores."""
        try:
            # Weight domains equally for now
            weights = {domain: 1.0 / len(self.LIFE_DOMAINS) for domain in self.LIFE_DOMAINS}
            
            overall_score = sum(
                score * weights[domain]
                for domain, score in domain_scores.items()
            )
            
            return round(overall_score * 100, 2)  # Convert to percentage
        except Exception as e:
            logger.error(f"Error calculating overall score: {str(e)}")
            return 0.0

    async def _generate_balance_insights(self, domain_scores: Dict[str, float], activities: List[Dict]) -> List[str]:
        """Generate insights about life balance based on scores and activities."""
        try:
            # Prepare data for analysis
            scores_text = "\n".join([f"{domain}: {score:.2f}" for domain, score in domain_scores.items()])
            activities_text = "\n".join([
                f"Activity: {activity['type']}, Duration: {activity['duration']}"
                for activity in activities[:10]  # Limit to recent activities
            ])
            
            prompt = f"""
            Analyze the following life balance data and provide key insights:
            
            Domain Scores:
            {scores_text}
            
            Recent Activities:
            {activities_text}
            
            Provide 3-5 specific, actionable insights about the person's life balance.
            Focus on patterns, areas needing attention, and positive aspects.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI life coach analyzing work-life balance data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            insights = response.choices[0].message.content.strip().split('\n')
            return [insight.strip('- ') for insight in insights if insight.strip()]
        except Exception as e:
            logger.error(f"Error generating balance insights: {str(e)}")
            return ["Unable to generate insights at this time."]

    async def generate_recommendations(self, domain_scores: Dict[str, float], activities: List[Dict]) -> List[Dict]:
        """Generate personalized recommendations for improving life balance."""
        try:
            # Identify domains needing improvement
            low_scoring_domains = [
                domain for domain, score in domain_scores.items()
                if score < 0.6  # Threshold for considering a domain as needing improvement
            ]
            
            recommendations = []
            for domain in low_scoring_domains:
                prompt = f"""
                Generate a specific, actionable recommendation for improving the '{domain}' aspect of life balance.
                Consider current activities and make the suggestion practical and achievable.
                Include both what to do and how to implement it.
                """
                
                response = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI life coach providing practical recommendations."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                
                recommendation = response.choices[0].message.content.strip()
                recommendations.append({
                    'domain': domain,
                    'recommendation': recommendation,
                    'priority': 'high' if domain_scores[domain] < 0.4 else 'medium'
                })
            
            return recommendations
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return []

    async def assess_burnout_risk(self, activities: List[Dict], domain_scores: Dict[str, float]) -> Dict:
        """Assess risk of burnout based on activity patterns and balance scores."""
        try:
            # Calculate work-related metrics
            work_activities = [a for a in activities if self._map_activity_to_domain(a['type']) == 'work']
            total_work_time = sum(a['duration'] for a in work_activities)
            
            # Calculate rest and recovery metrics
            rest_activities = [
                a for a in activities 
                if self._map_activity_to_domain(a['type']) in ['recreation', 'health']
            ]
            total_rest_time = sum(a['duration'] for a in rest_activities)
            
            # Prepare data for AI analysis
            data = {
                'work_time': total_work_time,
                'rest_time': total_rest_time,
                'work_score': domain_scores.get('work', 0),
                'health_score': domain_scores.get('health', 0),
                'recreation_score': domain_scores.get('recreation', 0)
            }
            
            prompt = f"""
            Assess burnout risk based on the following data:
            - Work time: {data['work_time']} hours
            - Rest time: {data['rest_time']} hours
            - Work-life balance scores:
              * Work domain: {data['work_score']:.2f}
              * Health domain: {data['health_score']:.2f}
              * Recreation domain: {data['recreation_score']:.2f}
            
            Provide:
            1. Risk level (low, medium, high)
            2. Key contributing factors
            3. Early warning signs to watch for
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI analyzing burnout risk factors."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.5
            )
            
            analysis = response.choices[0].message.content.strip().split('\n')
            
            # Calculate numerical risk score (0-1)
            risk_score = 1.0 - (data['rest_time'] / (data['work_time'] + 1e-6))  # Avoid division by zero
            risk_score = min(max(risk_score, 0.0), 1.0)  # Clamp between 0 and 1
            
            return {
                'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low',
                'risk_score': round(risk_score, 2),
                'analysis': analysis,
                'contributing_factors': [
                    factor.strip('- ') for factor in analysis 
                    if factor.strip() and not factor.startswith(('Risk', 'Warning'))
                ]
            }
        except Exception as e:
            logger.error(f"Error assessing burnout risk: {str(e)}")
            return {
                'risk_level': 'unknown',
                'risk_score': 0.0,
                'analysis': ["Unable to assess burnout risk at this time."],
                'contributing_factors': []
            }

    async def optimize_schedule(self, current_schedule: List[Dict], preferences: Dict) -> List[Dict]:
        """
        Optimize daily/weekly schedule for better life balance.
        
        Args:
            current_schedule: List of scheduled activities
            preferences: User preferences and constraints
            
        Returns:
            List of optimized schedule recommendations
        """
        try:
            # Prepare schedule data for analysis
            schedule_text = "\n".join([
                f"Activity: {item['type']}, Time: {item['time']}, Duration: {item['duration']}"
                for item in current_schedule
            ])
            
            preferences_text = "\n".join([
                f"{key}: {value}" for key, value in preferences.items()
            ])
            
            prompt = f"""
            Optimize the following schedule for better work-life balance:
            
            Current Schedule:
            {schedule_text}
            
            User Preferences:
            {preferences_text}
            
            Provide specific recommendations for schedule adjustments that would improve balance while respecting preferences.
            Include both what to change and why.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI schedule optimizer focused on improving work-life balance."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            recommendations = response.choices[0].message.content.strip().split('\n')
            
            return [
                {
                    'change': rec.strip('- '),
                    'impact': 'high',  # Could be calculated based on balance improvement
                    'feasibility': 'medium'  # Could be calculated based on preferences
                }
                for rec in recommendations if rec.strip()
            ]
        except Exception as e:
            logger.error(f"Error optimizing schedule: {str(e)}")
            return [] 