"""
Memory AI Service Module

This module provides AI-powered memory and learning optimization features:
- Memory pattern analysis
- Learning style identification
- Study schedule optimization
- Knowledge retention tracking
- Personalized learning recommendations
"""

import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import openai
import numpy as np
from sklearn.cluster import KMeans
from app.utils.logger import get_logger

logger = get_logger(__name__)

class MemoryAI:
    def __init__(self):
        """Initialize the Memory AI service."""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key
        
        # Define learning styles
        self.LEARNING_STYLES = {
            'visual': ['diagrams', 'charts', 'videos', 'mind_maps'],
            'auditory': ['lectures', 'discussions', 'audio_books', 'verbal_explanations'],
            'kinesthetic': ['hands_on', 'experiments', 'role_playing', 'physical_activities'],
            'reading_writing': ['textbooks', 'notes', 'articles', 'written_exercises']
        }
        
        # Memory enhancement techniques
        self.MEMORY_TECHNIQUES = {
            'spaced_repetition': {
                'intervals': [1, 3, 7, 14, 30],  # Days between reviews
                'retention_threshold': 0.8
            },
            'active_recall': {
                'question_types': ['multiple_choice', 'short_answer', 'explanation'],
                'difficulty_levels': ['easy', 'medium', 'hard']
            },
            'mind_mapping': {
                'max_branches': 7,
                'levels': 3
            }
        }

    async def analyze_learning_patterns(self, study_sessions: List[Dict]) -> Dict:
        """
        Analyze learning patterns and provide insights for optimization.
        
        Args:
            study_sessions: List of study session records with type, duration, performance
            
        Returns:
            Dict containing learning analysis, patterns, and recommendations
        """
        try:
            # Analyze learning style preferences
            learning_style = await self._identify_learning_style(study_sessions)
            
            # Calculate performance metrics
            performance_metrics = self._calculate_performance_metrics(study_sessions)
            
            # Generate learning insights
            insights = await self._generate_learning_insights(study_sessions, learning_style)
            
            # Get optimization recommendations
            recommendations = await self.generate_study_recommendations(
                study_sessions, 
                learning_style,
                performance_metrics
            )
            
            return {
                'learning_style': learning_style,
                'performance_metrics': performance_metrics,
                'insights': insights,
                'recommendations': recommendations,
                'analyzed_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing learning patterns: {str(e)}")
            raise

    async def _identify_learning_style(self, study_sessions: List[Dict]) -> Dict[str, float]:
        """Identify preferred learning styles based on study session data."""
        try:
            # Initialize style scores
            style_scores = {style: 0.0 for style in self.LEARNING_STYLES.keys()}
            total_duration = sum(session['duration'] for session in study_sessions)
            
            # Calculate style preferences based on activity types
            for session in study_sessions:
                activity_type = session['type'].lower()
                duration = session['duration']
                performance = session.get('performance', 0.5)
                
                for style, activities in self.LEARNING_STYLES.items():
                    if any(activity in activity_type for activity in activities):
                        # Weight score by duration and performance
                        style_scores[style] += (duration * performance)
            
            # Normalize scores
            if total_duration > 0:
                for style in style_scores:
                    style_scores[style] /= total_duration
                    style_scores[style] = round(style_scores[style], 3)
            
            return style_scores
        except Exception as e:
            logger.error(f"Error identifying learning style: {str(e)}")
            return {style: 0.0 for style in self.LEARNING_STYLES.keys()}

    def _calculate_performance_metrics(self, study_sessions: List[Dict]) -> Dict:
        """Calculate various performance metrics from study sessions."""
        try:
            if not study_sessions:
                return {
                    'average_performance': 0.0,
                    'trend': 'neutral',
                    'best_performing_topics': [],
                    'needs_improvement': []
                }
            
            # Calculate average performance
            performances = [s.get('performance', 0) for s in study_sessions]
            avg_performance = np.mean(performances)
            
            # Calculate performance trend
            trend = 'improving' if len(performances) > 1 and performances[-1] > performances[0] else 'declining'
            
            # Analyze performance by topic
            topic_performances = {}
            for session in study_sessions:
                topic = session.get('topic', 'unknown')
                if topic not in topic_performances:
                    topic_performances[topic] = []
                topic_performances[topic].append(session.get('performance', 0))
            
            # Calculate average performance by topic
            topic_averages = {
                topic: np.mean(perfs)
                for topic, perfs in topic_performances.items()
            }
            
            # Identify best and worst performing topics
            sorted_topics = sorted(
                topic_averages.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            return {
                'average_performance': round(avg_performance, 3),
                'trend': trend,
                'best_performing_topics': [t[0] for t in sorted_topics[:3]],
                'needs_improvement': [t[0] for t in sorted_topics[-3:]]
            }
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {str(e)}")
            return {
                'average_performance': 0.0,
                'trend': 'neutral',
                'best_performing_topics': [],
                'needs_improvement': []
            }

    async def _generate_learning_insights(self, 
                                        study_sessions: List[Dict],
                                        learning_style: Dict[str, float]) -> List[str]:
        """Generate insights about learning patterns and effectiveness."""
        try:
            # Prepare data for analysis
            style_text = "\n".join([
                f"{style}: {score:.2f}" 
                for style, score in learning_style.items()
            ])
            
            sessions_text = "\n".join([
                f"Topic: {session.get('topic', 'unknown')}, "
                f"Type: {session['type']}, "
                f"Performance: {session.get('performance', 0):.2f}"
                for session in study_sessions[-5:]  # Last 5 sessions
            ])
            
            prompt = f"""
            Analyze the following learning data and provide key insights:
            
            Learning Style Preferences:
            {style_text}
            
            Recent Study Sessions:
            {sessions_text}
            
            Provide 3-5 specific insights about learning patterns and effectiveness.
            Focus on strengths, areas for improvement, and notable patterns.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI learning coach analyzing study patterns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            insights = response.choices[0].message.content.strip().split('\n')
            return [insight.strip('- ') for insight in insights if insight.strip()]
        except Exception as e:
            logger.error(f"Error generating learning insights: {str(e)}")
            return ["Unable to generate learning insights at this time."]

    async def generate_study_recommendations(self,
                                          study_sessions: List[Dict],
                                          learning_style: Dict[str, float],
                                          performance_metrics: Dict) -> List[Dict]:
        """Generate personalized study recommendations."""
        try:
            # Identify primary learning style
            primary_style = max(learning_style.items(), key=lambda x: x[1])[0]
            
            # Prepare data for recommendations
            data = {
                'learning_style': primary_style,
                'performance': performance_metrics['average_performance'],
                'improvement_areas': performance_metrics['needs_improvement'],
                'recent_sessions': study_sessions[-5:]  # Last 5 sessions
            }
            
            prompt = f"""
            Generate specific study recommendations based on:
            
            Learning Style: {data['learning_style']}
            Average Performance: {data['performance']:.2f}
            Areas Needing Improvement: {', '.join(data['improvement_areas'])}
            
            Provide 3 specific, actionable recommendations that:
            1. Align with the learning style
            2. Address improvement areas
            3. Include specific techniques or methods
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI learning coach providing personalized study recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            recommendations = response.choices[0].message.content.strip().split('\n')
            return [
                {
                    'recommendation': rec.strip('- '),
                    'style_alignment': primary_style,
                    'priority': 'high' if idx == 0 else 'medium'
                }
                for idx, rec in enumerate(recommendations) if rec.strip()
            ]
        except Exception as e:
            logger.error(f"Error generating study recommendations: {str(e)}")
            return []

    async def optimize_retention(self, 
                               topic: str,
                               content: str,
                               learning_history: Optional[List[Dict]] = None) -> Dict:
        """
        Generate optimized retention strategy for learning content.
        
        Args:
            topic: The subject or topic being studied
            content: The learning content or material
            learning_history: Optional list of previous learning sessions
            
        Returns:
            Dict containing retention strategy and review schedule
        """
        try:
            # Generate key concepts and summary
            concepts = await self._extract_key_concepts(topic, content)
            
            # Create review questions
            review_questions = await self._generate_review_questions(
                topic,
                content,
                concepts
            )
            
            # Calculate optimal review intervals
            review_schedule = self._calculate_review_schedule(
                learning_history or [],
                len(concepts)
            )
            
            # Generate retention techniques
            retention_techniques = await self._recommend_retention_techniques(
                topic,
                concepts
            )
            
            return {
                'key_concepts': concepts,
                'review_questions': review_questions,
                'review_schedule': review_schedule,
                'retention_techniques': retention_techniques,
                'generated_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing retention: {str(e)}")
            raise

    async def _extract_key_concepts(self, topic: str, content: str) -> List[Dict]:
        """Extract and structure key concepts from learning content."""
        try:
            prompt = f"""
            Extract key concepts from the following {topic} content.
            For each concept, provide:
            1. The concept name/title
            2. A brief explanation
            3. Its importance or relevance
            
            Content:
            {content[:1000]}  # Limit content length
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI extracting and structuring key learning concepts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.5
            )
            
            # Parse response into structured concepts
            concepts_text = response.choices[0].message.content.strip().split('\n\n')
            concepts = []
            
            for concept_text in concepts_text:
                if not concept_text.strip():
                    continue
                    
                lines = concept_text.strip().split('\n')
                if len(lines) >= 2:
                    concepts.append({
                        'title': lines[0].strip('- '),
                        'explanation': lines[1].strip(),
                        'importance': lines[2].strip() if len(lines) > 2 else ''
                    })
            
            return concepts
        except Exception as e:
            logger.error(f"Error extracting key concepts: {str(e)}")
            return []

    async def _generate_review_questions(self,
                                      topic: str,
                                      content: str,
                                      concepts: List[Dict]) -> List[Dict]:
        """Generate review questions for effective recall practice."""
        try:
            questions = []
            
            for concept in concepts:
                prompt = f"""
                Generate 2 review questions for the following concept in {topic}:
                
                Concept: {concept['title']}
                Explanation: {concept['explanation']}
                
                Create:
                1. One multiple-choice question
                2. One open-ended question
                Include correct answers and explanations.
                """
                
                response = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI creating effective review questions for learning."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                
                question_text = response.choices[0].message.content.strip()
                question_parts = question_text.split('\n\n')
                
                for part in question_parts:
                    if not part.strip():
                        continue
                        
                    lines = part.strip().split('\n')
                    questions.append({
                        'concept': concept['title'],
                        'question': lines[0].strip('Q: '),
                        'type': 'multiple_choice' if 'a)' in part.lower() else 'open_ended',
                        'answer': lines[-1].strip('A: '),
                        'explanation': lines[-2].strip('Explanation: ') if len(lines) > 2 else ''
                    })
            
            return questions
        except Exception as e:
            logger.error(f"Error generating review questions: {str(e)}")
            return []

    def _calculate_review_schedule(self, 
                                 learning_history: List[Dict],
                                 num_concepts: int) -> List[Dict]:
        """Calculate optimal review schedule based on spaced repetition."""
        try:
            base_intervals = self.MEMORY_TECHNIQUES['spaced_repetition']['intervals']
            
            # Calculate initial review date
            start_date = datetime.utcnow()
            
            # Generate review schedule
            schedule = []
            for interval in base_intervals:
                review_date = start_date + timedelta(days=interval)
                
                schedule.append({
                    'review_date': review_date.isoformat(),
                    'interval_days': interval,
                    'estimated_duration': max(30, num_concepts * 5),  # 5 minutes per concept
                    'review_type': 'comprehensive' if interval > 7 else 'quick',
                    'concepts_to_review': num_concepts
                })
            
            return schedule
        except Exception as e:
            logger.error(f"Error calculating review schedule: {str(e)}")
            return []

    async def _recommend_retention_techniques(self, topic: str, concepts: List[Dict]) -> List[Dict]:
        """Recommend specific techniques for better retention of the material."""
        try:
            prompt = f"""
            Recommend specific retention techniques for learning {topic} with {len(concepts)} key concepts.
            
            Concepts:
            {', '.join(c['title'] for c in concepts)}
            
            Provide 3-4 specific techniques that:
            1. Are appropriate for the topic
            2. Can be practically implemented
            3. Include specific steps or methods
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI recommending memory retention techniques."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            techniques = response.choices[0].message.content.strip().split('\n')
            return [
                {
                    'technique': tech.strip('- '),
                    'difficulty': 'medium',
                    'effectiveness': 'high',
                    'time_required': 15  # minutes, default value
                }
                for tech in techniques if tech.strip()
            ]
        except Exception as e:
            logger.error(f"Error recommending retention techniques: {str(e)}")
            return []

    async def analyze_knowledge_gaps(self, 
                                   topic: str,
                                   content: str,
                                   assessment_results: List[Dict]) -> Dict:
        """
        Analyze knowledge gaps and provide targeted recommendations.
        
        Args:
            topic: The subject being studied
            content: The learning material
            assessment_results: List of previous assessment results
            
        Returns:
            Dict containing gap analysis and improvement strategies
        """
        try:
            # Identify knowledge gaps
            gaps = await self._identify_knowledge_gaps(
                topic,
                content,
                assessment_results
            )
            
            # Generate focused learning plan
            learning_plan = await self._generate_gap_learning_plan(
                topic,
                gaps
            )
            
            # Recommend resources
            resources = await self._recommend_gap_resources(
                topic,
                gaps
            )
            
            return {
                'identified_gaps': gaps,
                'learning_plan': learning_plan,
                'recommended_resources': resources,
                'analyzed_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing knowledge gaps: {str(e)}")
            raise

    async def _identify_knowledge_gaps(self,
                                     topic: str,
                                     content: str,
                                     assessment_results: List[Dict]) -> List[Dict]:
        """Identify specific knowledge gaps from assessment results."""
        try:
            # Analyze assessment results
            weak_areas = [
                result for result in assessment_results
                if result.get('score', 0) < 0.7  # Threshold for identifying gaps
            ]
            
            # Generate gap analysis
            gaps = []
            for area in weak_areas:
                prompt = f"""
                Analyze this weak performance area in {topic}:
                
                Topic: {area.get('subtopic', 'unknown')}
                Score: {area.get('score', 0):.2f}
                Details: {area.get('details', '')}
                
                Identify:
                1. Specific concepts not well understood
                2. Potential reasons for the gap
                3. Prerequisites that might need review
                """
                
                response = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI analyzing learning gaps."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.5
                )
                
                analysis = response.choices[0].message.content.strip().split('\n')
                gaps.append({
                    'subtopic': area.get('subtopic', 'unknown'),
                    'concepts': [line.strip('- ') for line in analysis if line.strip()],
                    'severity': 'high' if area.get('score', 0) < 0.5 else 'medium'
                })
            
            return gaps
        except Exception as e:
            logger.error(f"Error identifying knowledge gaps: {str(e)}")
            return [] 