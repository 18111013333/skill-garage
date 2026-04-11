---
name: JavaScript
license: MIT
description: >
  A comprehensive JavaScript style guide skill.
  When activated, it provides best-practice JavaScript coding conventions and generates
  code that strictly follows the style guide, covering variables, functions, objects,
  arrays, classes, modules, async patterns, error handling, naming conventions, and more.
---

# JavaScript Style Guide Skill

## Activation

This skill activates when the user mentions or implies **JavaScript** in their request. Once activated, it:

- Responds with best-practice guidance
- Generates JavaScript code that strictly conforms to the style guide
- Provides explanations for why each convention is recommended

---

## Complete Style Rules

### 1. References

- Use `const` for all references; avoid `var`.
- If you must reassign references, use `let` instead of `var`.
- Both `const` and `let` are block-scoped, whereas `var` is function-scoped.

```javascript
// bad
var count = 1;

// good
const count = 1;
let mutableValue = 1;
mutableValue += 1;
```

### 2. Objects

- Use literal syntax for object creation.
- Use computed property names when creating objects with dynamic property names.
- Use object method shorthand and property value shorthand.
- Group shorthand properties at the beginning of the object declaration.
- Only quote properties that are invalid identifiers.
- Prefer the object spread syntax (`...`) over `Object.assign` to shallow-copy objects.

```javascript
// bad
const item = new Object();

// good
const item = {};

// computed property names
const key = 'name';
const obj = { [key]: 'value' };

// method & property shorthand
const name = 'Alice';
const atom = {
  name,
  value: 1,
  addValue(val) {
    return atom.value + val;
  },
};

// shallow copy
const original = { a: 1, b: 2 };
const copy = { ...original, c: 3 };
```

### 3. Arrays

- Use literal syntax for array creation.
- Use `Array.from` or the spread operator to convert array-like objects.
- Use `return` statements in array method callbacks.
- Use line breaks after the opening bracket and before the closing bracket if the array has multiple lines.

```javascript
// bad
const items = new Array();

// good
const items = [];

// convert iterable
const nodes = Array.from(document.querySelectorAll('.item'));
const uniqueValues = [...new Set(arr)];

// array methods
[1, 2, 3].map((x) => x + 1);

[1, 2, 3].map((x) => {
  const y = x + 1;
  return x * y;
});

## 详细文档

请参阅 [references/details.md](references/details.md)
