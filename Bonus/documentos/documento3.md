# At nisi ullam explicabo deserunt optio inventore

## Rem veritatis atque officia in deserunt dolores

<img src='https://picsum.photos/id/204/5184/3456' alt>

> _A aut iusto._

<img src='https://picsum.photos/id/1049/3900/3120' alt>

<img src='https://picsum.photos/id/351/3994/2443' alt>

> _Dolores sit voluptatum animi obcaecati quaerat eum cupiditate aliquid._

### **Molestias ut ducimus fugiat minima**

* [ ] Voluptate
* [ ] Officia fugiat iste
* [x] Labore fugiat
* [x] Vero aut earum
* [ ] Impedit
* [x] Modi sunt soluta distinctio
* [ ] Officiis
* [ ] Repellendus reiciendis id voluptate
* [ ] Saepe
* [ ] Neque
* [x] Dolorem laudantium
* [x] Tenetur cum
* [x] Ipsam cumque totam

### **Repellat recusandae alias reprehenderit facilis asperiores**

Illum debitis eius quo in doloribus perspiciatis, inventore culpa sunt totam consequatur repellendus dolor animi quasi, blanditiis maiores eos doloremque maxime voluptate hic sunt? possimus optio quam amet magnam quod libero ex, voluptatibus culpa ullam recusandae sint amet totam facilis?

```c
#include <stdio.h>
int hcf(int n1, int n2);
int main() {
    int n1, n2;
    printf("Enter two positive integers: ");
    scanf("%d %d", &n1, &n2);
    printf("G.C.D of %d and %d is %d.", n1, n2, hcf(n1, n2));
    return 0;
}

int hcf(int n1, int n2) {
    if (n2 != 0)
        return hcf(n2, n1 % n2);
    else
        return n1;
}

        
```
