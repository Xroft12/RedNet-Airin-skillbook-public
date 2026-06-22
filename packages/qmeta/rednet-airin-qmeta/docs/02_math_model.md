# Математическая модель

Пусть пространство ветвей:

```text
H_B = span{|b_1>, |b_2>, ..., |b_n>}
```

Состояние агента:

```text
|Ψ_t> = Σ_i α_i^(t) |b_i^(t)>,    Σ_i |α_i|² = 1
```

Ветвь:

```text
b_i = (x_i, e_i, r_i, c_i, τ_i)
```

где:

- `x_i` — содержимое;
- `e_i` — evidence;
- `r_i` — риск-профиль;
- `c_i` — ограничения;
- `τ_i` — trace.

Комплексная амплитуда:

```text
α_i = ρ_i exp(i φ_i)
```

Вероятность выбора:

```text
p_i = |α_i|² / Σ_j |α_j|²
```

Loss:

```text
loss_i = λ_h H_i + λ_s S_i + λ_r R_i
```

Интерференция:

```text
G_ij = kernel(signature_i, signature_j)
u_i = score_i - loss_i + γ Σ_{j≠i} G_ij score_j - η contradiction_i
α_i' = sqrt(softmax(βu_i)) exp(iφ_i)
```

Измерение:

```text
i* = argmax_i |α_i|²
```

Результат:

```text
O_mode(Ψ,C) = Rω(Ψ,i*,C), если mode=answer
O_mode(Ψ,C) = Qψ(τ_i*,C), если mode=skill
```
