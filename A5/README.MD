# A5: Reflect — Group 07

**Course:** 41934 Advanced Building Information Modeling  
**Group:** 07  
**Focus area:** Fire evacuation / egress  
**Project:** IFC Fire-Egress Information Checker

---

# 1. Learning Experience

Throughout the course, our group focused on how OpenBIM and IFC information can support fire-evacuation analysis.

One of the most important things we learned is that having geometry in an IFC model does not necessarily mean that the model contains enough information for reliable automated analysis.

For example, a model may contain doors, spaces and stairs, but still lack important information such as:

- `Pset_DoorCommon.FireExit`
- fire-safety properties
- `IfcRelSpaceBoundary`
- reliable connections between spaces and doors
- documented clear widths

This changed the way we understood BIM automation. Instead of immediately trying to calculate evacuation routes, we learned that the first step should be to check whether the required information is actually available.

At the beginning of the course, our understanding of OpenBIM was mainly focused on using and viewing IFC models. We had limited experience using Python and IfcOpenShell to directly investigate IFC entities, attributes, property sets and relationships.

During the course, we became more confident with:

- opening IFC files using IfcOpenShell;
- using `model.by_type()` to find IFC entities;
- reading IFC attributes and property sets;
- identifying missing BIM information;
- using Python to automate model checks;
- reporting results without making unsupported assumptions.

We would therefore describe our development as moving from mainly a **Modeller / beginning Analyst level** toward a stronger **Analyst / Self Learner level**.

---

# 2. What We Still Need to Learn

There are still several areas that we would like to develop further.

The main one is IFC connectivity.

For fire evacuation analysis, it is not enough to know that spaces and doors exist. We also need to understand how spaces, doors, stairs and storeys are connected.

We would therefore like to learn more about:

- IFC relationships between spaces and building elements;
- `IfcRelSpaceBoundary`;
- building evacuation networks from IFC information
- calculating actual evacuation-route distances;
- validating information requirements using IDS;
- making OpenBIM tools work reliably across different IFC models.

Our current work mainly checks whether the information needed for analysis is available. A future development could use this information to construct a complete evacuation network and calculate routes.

---

# 3. Process of Developing the A3 Tutorial

For A3, we developed the tutorial:

**Checking IFC Fire-Egress Data with IfcOpenShell**

The learning need was:

> How can a BIM analyst use Python and IfcOpenShell to determine whether an IFC model contains sufficient fire-egress information before attempting automated route analysis?

We created the tutorial in two formats:

1. Markdown tutorial
2. Jupyter Notebook

The Markdown tutorial was designed as a written step-by-step reference.

The Jupyter Notebook was designed as a more interactive version where students could execute Python code directly and observe the results.

Developing the tutorial helped us understand the topic better ourselves. Explaining the workflow to another student forced us to simplify the code and explain why each IFC entity or property was important.

One of the most important teaching points became the difference between:

```text
PASS / FAIL
```

and:

```text
INSUFFICIENT DATA
```

We learned that an automated BIM tool should not force a pass/fail result when the required IFC information is missing.

---

# 4. Reflection on the Course Process

The course process helped us understand how a broad architectural issue can gradually become an OpenBIM use case.

We started with a general topic of fire evacuation and gradually narrowed it down into measurable information requirements.

The process can be summarised as:

```text
Identify a problem
↓
Define a use case
↓
Identify information requirements
↓
Inspect available BIM information
↓
Develop an automated method
↓
Test and evaluate the result
```

We think this process could also be useful for a future thesis because it provides a structured way of developing a research or design question.

We think having freedom in choosing the use case was useful because it allowed us to work with a topic that was relevant to our architectural interests.

However, some example use cases at the beginning could also have helped make the first stages easier.

The number of tools introduced during the course was useful, although at times it was challenging to learn several new concepts at once.

For our project, Python and IfcOpenShell were the most important tools because they allowed us to directly inspect and process IFC information.

---

# 5. Group Reflection on Feedback

We received positive feedback on our A3 tutorial.

The group found the tutorial **well structured and easy to understand**, and they especially liked that we explained the different steps clearly and showed examples of the results.

They also liked that we provided the tutorial in **two formats: a Markdown guide and a Jupyter Notebook**. This gave users two different ways of learning the workflow.

One suggestion was to include an example showing what the output looks like when the IFC model contains **sufficient data**.

At the moment, our tutorial mainly demonstrates the result:

```text
INSUFFICIENT DATA
```

The feedback suggested that it would be useful to also show:

```text
READY
```

We think this is a useful suggestion because showing both possible outcomes would make it easier for users to compare and understand the results.

Based on this feedback, we would improve the tutorial by adding an example of a model that passes the information-readiness check and showing the expected `READY` output.

Overall, the feedback confirmed that the structure and teaching approach worked well, while also identifying a simple improvement that could make the tutorial clearer and more complete.

---

# 6. Did the Tool Address the Use Case?

Partly.

The tool successfully addresses the **information-readiness part** of the fire-evacuation use case.

It can inspect whether relevant IFC information exists, including:

- fire-exit information;
- fire-related door properties;
- nominal door widths;
- stairs and stair flights;
- space-boundary relationships;
- relevant IFC geometry.

However, the tool does not yet prove full fire-evacuation compliance.

For example, it does not currently verify:

- complete evacuation-route connectivity;
- actual escape-route distances;
- effective clear widths in all cases;
- whether evacuation stairs are located correctly;
- full compliance with fire-safety regulations.

Therefore, the tool should be understood as an **IFC information and readiness checker**, rather than a complete fire-safety compliance tool.

This limitation is important because automated BIM tools should clearly distinguish between what has actually been verified and what has not been checked.

---

# 7. Stage in Advanced Building Design

Our tool is mainly relevant during the **design and design-review stages**, before the building is constructed.

At this stage, the IFC model can be checked to determine whether the required fire-egress information has been included.

If information is missing, the architect or BIM team can improve the model before later analysis or compliance checking is performed.

---

# 8. Individual Reflection — Member 1

**Name:** [Sarah]

My future use of OpenBIM

As an architecture student, I originally saw IFC mainly as a way of exchanging models between different software. During this course, I started to understand that IFC can also be used as a source of structured information that can be checked and analysed.

I could see myself using OpenBIM in a future thesis, especially if I work with BIM analysis, building performance or automated checking. In professional practice, I think it could be useful for finding missing information, checking models and supporting coordination between different disciplines.

I do not expect programming to become the main part of my work, but I now feel more confident understanding what tools such as Python and IfcOpenShell can do and how they can support architectural work.

Wrap-up

For me, the biggest change from A1 to A5 was learning to look beyond what is visible in the 3D model.

At the beginning, our fire-evacuation topic seemed mainly like a design and safety problem. As we worked through the assignments, I learned that automated analysis also depends heavily on how the information is structured inside the IFC.

A3 helped me understand the topic better because we had to explain it clearly to other students, while A4 showed me how the same ideas could actually be tested with Python and IfcOpenShell.

The main lesson I will take from the course is that a BIM model can look complete while still missing important information. This has made me more aware of the importance of information quality when using BIM for automated analysis.

---

# 9. Individual Reflection — Member 2

**Name:** [Mariam]

My future use of BIM

I would consider using OpenBIM in my thesis, but I am still exploring different directions. Even if I do not end up working directly with BIM, this course has made me realise that I could use similar tools and approaches to find solutions within some of the other areas I am interested in. I think this could be especially useful in interdisciplinary projects, where people work on the same project but focus on different things.

I would like to go in a more humanitarian direction with my engineering degree, so I expect to work more with calculations and analysis than modelling. However, I find OpenBIM quite interesting, and I would not rule out using it in my professional life within the next 10 years. I think some of the things we have learned could make certain tasks easier and help people from different disciplines work together.

Wrap up

When we started with A1, my knowledge was mainly limited to working with Blender. In a previous course, we had already been introduced to the benefits of making building information more accessible to people working on the same model.

During A1 and A2, my previous experience with Blender made it easier for me to identify some of the problems in the IFC model. However, identifying a problem and knowing how to solve it were two different things.

Through A3 and A4, I started to understand how we could approach these problems and which tools we could use to find possible solutions. I also learned a lot more about programming and the different tools available within OpenBIM.

Looking back at the journey from A1 to A5, one of my main takeaways is that taking the first step towards solving a problem can sometimes be easier than expected. It does not necessarily mean that the entire problem has been solved, but it provides a starting point for further development. The course has given me a better understanding of how digital tools and programming can support problem-solving in engineering, even beyond BIM.


---

# 10. Individual Reflection — Member 3

**Name:** [Eda]



---

# 11. Future Use of OpenBIM

We believe OpenBIM could be useful both academically and professionally.

In a thesis, OpenBIM could support:

- automated compliance checking;
- fire-safety analysis;
- accessibility analysis;
- information-quality assessment;
- design optimisation.

In professional practice, OpenBIM could support:

- BIM quality control;
- design review;
- model checking;
- interdisciplinary coordination;
- automated information checks.

The course has made us more aware that IFC is not only an exchange format, but also a structured data source that can be used for automated analysis.

---

# 12. Wrap-up — A1 to A5

The assignments gradually developed our understanding of OpenBIM.

## A1 — Understand the model

We investigated Building 308 and identified limitations in the available fire-evacuation information.

We found that the model contained relevant building elements, but some information needed for reliable fire-egress analysis was missing.

## A2 — Define the use case

We translated the fire-evacuation problem into an OpenBIM use case.

We identified the information required for automated checking and considered how Python and IfcOpenShell could support the analysis.

## A3 — Teach

We created two tutorial formats:

- a Markdown tutorial;
- a Jupyter Notebook.

The tutorials teach BIM analysts how to inspect IFC fire-egress information using IfcOpenShell and determine whether the model contains sufficient information for further automated analysis.

## A4 — Implement

We developed a Python-based IFC fire-egress checker.

The tool inspects relevant IFC classes, properties, widths, geometry and information availability.

The tool also makes clear which requirements are **not verified** rather than making unsupported assumptions.

## A5 — Reflect

Finally, we reflected on what the complete process taught us about OpenBIM, automation and information quality.

An automated tool should not produce conclusions that are stronger than the information contained in the model.

Sometimes the most useful result is not:

**PASS**

or:

**FAIL**

but:

**INSUFFICIENT DATA**

This is an important principle that we expect to carry into future OpenBIM work.
