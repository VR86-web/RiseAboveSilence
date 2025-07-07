## 🧩 Mixins

Mixins are reusable components designed to add common behavior to Django forms or views without duplicating code.

---

### 🛑 Mixin: DisableFieldsMixin

**Overview**

`DisableFieldsMixin` is a form mixin designed to automatically **disable fields in a form when displaying confirmation pages**, such as deletion forms. This ensures that users can see the field values but cannot edit them.

This mixin is used in:

- **Profile Delete Form**
- **Post Delete Form**

---

#### 🧰 How It Works

When included in a form class, this mixin inspects all form fields in `__init__()`. For any field listed in `disabled_fields`, the field is set to `disabled=True`, making it read-only in the rendered form.

---

#### ⚙️ Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `disabled_fields` | `tuple` | Specifies which fields to disable. Use `("__all__",)` to disable all fields in the form. |

---

#### 📘 Example Usage

```python
class PostDeleteForm(DisableFieldsMixin, forms.ModelForm):
    disabled_fields = ("__all__",)

    class Meta:
        model = Post
        fields = ["title", "content", "created_at"]
