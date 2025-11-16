## LLM Fine-Tuning

This repository contains the code, data, and documentation for a data science project that investigates whether a Large Language Model (LLM) can be fine-tuned to consistently generate a specific style of humor. In this case, over-the-top "Chuck Norris jokes" related to any subject. The project involves collecting a dataset of Chuck Norris jokes, transforming the data for training, and applying supervised fine-tuning techniques to teach the LLM to append a relevant joke to factual responses about any topic.

The end goal is a chatbot that responds to prompts for random facts about any subject and adds a brief, topic-related Chuck Norris joke with the expected format and humorous exaggeration. Evaluation demonstrates that the fine-tuned model not only replicates jokes from the dataset but generates new, context-appropriate jokes for topics not included in training, validating the approach and usefulness of custom humor instruction for generative AI.

#### Skills
 - Data Acquisition & Preparation: Locating relevant datasets (e.g., Kaggle), cleaning data, and transforming formats for LLM fine-tuning.
 - Prompt Engineering: Designing effective prompts to extract and format information from LLMs, including identifying subjects and facts from joke lines.
 - Python Programming: Writing scripts for data processing, model training, logging metrics, and automating workflow.
 - API Integration: Utilizing OpenAI SDK for file uploads, model fine-tuning, and job status polling.
 - Model Fine-Tuning: Configuring and running supervised fine-tuning jobs, monitoring performance, and evaluating metrics such as training loss and mean token accuracy.
 - Data Analysis: Extracting performance metrics, writing results to CSV, and interpreting model behavior and generalization.
 - Experimentation & Evaluation: Designing comparative experiments to assess differences between base and fine-tuned models.
 - Documentation: Clearly documenting project goals, methodology, code, and results for reproducibility and sharing on platforms like GitHub.
