# Data Tables

## `irreducible_polys/`

Source: Gary L. Mullen, Daniel Panario, David Thomson

https://people.math.carleton.ca/~daniel/hff/

> This section is devoted to giving the (monic) lowest weight irreducible polynomial over GF(q) of lowest lexicographical order, where q &le; 27. For reliability, we use a brute force method: we exhaustively search through binomials (if applicable), followed by trinomials, tetranomials (if applicable) and pentanomials. In all cases, we observe that we need not search for polynomials with more than five terms. To check irreducibility, we use the deterministic iterative irreducibility test in NTL.
>
> The output always begins with the degree of the polynomial.
>
> Over GF(2), the comma-separated output lists the degree, followed by the degree of the terms with non-zero coefficients, not including the constant term (which is necessarily 1).
>
> For higher characteristics, the comma-separated output lists the degree, followed by the degree of the terms with non-zero coefficients and the coefficient (in NTL-readable format) enclosed in brackets.
>
> If the base field is GF(p<sup>n</sup>) with n > 1, then the first line of the output gives the defining polynomial of the field.
