# Document QA Bot User Guide

The Document QA Bot is an interactive application that allows you to upload documents and ask questions about their content. This guide will walk you through the process of using the bot.

## Getting Started

1. Open the Document QA Bot application in your web browser.
2. You'll see a main area and a sidebar for configuration.

## Configuration

1. In the sidebar, enter your Groq API Key and Pinecone API Key in the respective text fields.
2. Enter a name for your Vector Index Database.
3. Use the slider to set the number of top results to retrieve (default is 3).
4. Click the "Initialize" button to set up the application.

## Uploading a Document

1. Once initialized, you'll see a file uploader in the main area.
2. Click "Choose a document" to select a file from your computer.
   - Supported file types: PDF, DOCX, TXT, MD
3. After selecting a file, click the "Process Document" button.
4. Wait for the "Document processed and indexed successfully!" message.

## Asking Questions

1. Find the "Ask a question about your document:" text input field.
2. Type your question and press Enter.
3. The bot will process your question and provide an answer.

## Viewing Responses

1. The chat history will appear in the left column, showing your questions and the bot's answers.
2. In the right column, you'll see "Retrieved Content" for your last question.
3. Click on the expandable sections to view the relevant text chunks used to answer your question.

## Tips

- You can ask multiple questions about the same document without re-uploading it.
- The more specific your questions, the better the bot can provide relevant answers.
- If you're not satisfied with an answer, try rephrasing your question or asking for more details.

Remember, the quality of answers depends on the content of your uploaded document and the specificity of your questions. Enjoy using the Document QA Bot!
