You are a meticulous user researcher. Your goal is to identify and extract all comments from the provided text that describe a personal account of a UX pain point.

### Definition of a UX Pain Point:
A UX pain point is any statement that expresses:
- A struggle, difficulty, or frustration.
- A request for a missing feature or tool.
- A complaint about something not working as expected.
- An inability to accomplish a goal or task.
- A wish for a different or better way to do something.
- A question seeking solutions that don't currently exist.
- A time-consuming or inefficient processes.
- Comparisons highlighting gaps in current solutions.

### Instructions:
1. Read the entire text provided below inside the triple quotes.
2. Identify every comment tag (`<C>`) that contains one or more UX pain points according to the definition above.
3. Your output must be a valid array of strings. 
4. Each string in the array must be the complete and unmodified content of a comment you have identified.
5. If you find no comments that contain a UX pain point, return an empty array: `[]`.
6. Do not include any explanation, preamble, or summary. Your entire response must consist only of the array.

### Text:
"""
<C id="C1" author="Secure_Tax84">
  <T>A tool for finding and/or validating ideas ?</T>
  Is there a tool to find validated ideas ? Or lets say i have an idea and i want to pay to get my idea validated quickly ?
</C>
  <C id="C2" author="fork_that" parent="C1">
    Many people consider paying customers the only way to validate an idea. So try and pre-sell people. But the reality is many things are pre-validated. If there are competitors in a market and are doing something pretty much the same but you've got a twist on the idea then it's pre-validated.
  </C>
    <C id="C2.1" author="Secure_Tax84" parent="C2">
      How can i validate that people want that twist ?
    </C>
      <C id="C2.1.1" author="fork_that" parent="C2.1">
        Build it, if they don't want that twist just remove it.
      </C>
        <C id="C2.1.1.1" author="Secure_Tax84" parent="C2.1.1">
          So there is no tool
        </C>
          <C id="C2.1.1.1.1" author="LouisDosBuzios" parent="C2.1.1.1">
            What kind of tool are you expecting exactly? Maybe you should build a tool for that ?
          </C>
          <C id="C2.1.1.1.2" author="sinsquare" parent="C2.1.1.1">
            Is a landing page creator the tool?
          </C>
            <C id="C2.1.1.1.2.1" author="Secure_Tax84" parent="C2.1.1.1.2">
              No, the user have the landing page and he needs to validate the idea. So not a creator
            </C>
"""